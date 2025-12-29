from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Dict, Iterable, Optional, Set

import httpx
from fastapi import Depends, HTTPException, Request, status

from app.clients.medplum import fetch_auth_me
from app.core.config import settings
from app.core.security import validate_jwt


class Role(StrEnum):
    PATIENT = "patient"
    CLINICIAN = "clinician"
    RESEARCH = "research"
    BACKEND_SERVICE = "backend_service"


@dataclass(frozen=True)
class UserContext:
    sub: str
    profile: Optional[str]
    role: Role
    token: str
    access_policy: Optional[str]
    project_id: Optional[str]


def _parse_identifier_list(value: Optional[str]) -> Set[str]:
    if not value:
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def _extract_reference(value: Any) -> Optional[str]:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        if "reference" in value and isinstance(value["reference"], str):
            return value["reference"]
        if value.get("resourceType") and value.get("id"):
            return f"{value['resourceType']}/{value['id']}"
    return None


def _extract_access_policy(auth_me: Optional[Dict[str, Any]]) -> Optional[str]:
    if not auth_me:
        return None

    for candidate in (
        auth_me.get("accessPolicy"),
        auth_me.get("projectMembership", {}).get("accessPolicy"),
        auth_me.get("membership", {}).get("accessPolicy"),
    ):
        ref = _extract_reference(candidate)
        if ref:
            return ref
        if isinstance(candidate, dict) and candidate.get("name"):
            return candidate["name"]
    return None


def _extract_profile(payload: Dict[str, Any], auth_me: Optional[Dict[str, Any]]) -> Optional[str]:
    if auth_me:
        for candidate in (
            auth_me.get("profile"),
            auth_me.get("projectMembership", {}).get("profile"),
            auth_me.get("membership", {}).get("profile"),
        ):
            ref = _extract_reference(candidate)
            if ref:
                return ref
    profile = payload.get("profile") or payload.get("fhirUser")
    if isinstance(profile, str):
        return profile
    return None


def _extract_project_id(auth_me: Optional[Dict[str, Any]]) -> Optional[str]:
    if not auth_me:
        return None
    for candidate in (auth_me.get("project"), auth_me.get("projectMembership", {}).get("project")):
        ref = _extract_reference(candidate)
        if ref:
            return ref.split("/")[-1]
    return None


def _resolve_role_from_policy(access_policy: Optional[str]) -> Optional[Role]:
    if not access_policy:
        return None

    policy_id = access_policy.split("/")[-1]
    identifiers = {access_policy, policy_id}

    role_map = {
        Role.PATIENT: _parse_identifier_list(settings.MEDPLUM_POLICY_PATIENT),
        Role.CLINICIAN: _parse_identifier_list(settings.MEDPLUM_POLICY_CLINICIAN),
        Role.RESEARCH: _parse_identifier_list(settings.MEDPLUM_POLICY_RESEARCH),
        Role.BACKEND_SERVICE: _parse_identifier_list(settings.MEDPLUM_POLICY_BACKEND_SERVICE),
    }

    for role, allowed in role_map.items():
        if identifiers & allowed:
            return role
    return None


def _resolve_role_from_profile(profile: Optional[str]) -> Optional[Role]:
    if not profile:
        return None
    if profile.startswith("Patient/"):
        return Role.PATIENT
    return None


async def get_user_context(
    request: Request, payload: Dict[str, Any] = Depends(validate_jwt)
) -> UserContext:
    token = payload.get("_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")

    if settings.STARVIT_MODE == "stub":
        role_header = request.headers.get("X-Starvit-Role", "").strip().lower()
        role_map = {
            "patient": Role.PATIENT,
            "clinician": Role.CLINICIAN,
            "research": Role.RESEARCH,
            "backend_service": Role.BACKEND_SERVICE,
        }
        role = role_map.get(role_header, Role.PATIENT)
        profile = request.headers.get("X-Starvit-Profile") or payload.get("profile")
        return UserContext(
            sub=payload.get("sub", "stub"),
            profile=profile,
            role=role,
            token=token,
            access_policy=None,
            project_id=None,
        )

    auth_me = None
    if settings.MEDPLUM_AUTH_ME_URL:
        try:
            auth_me = await fetch_auth_me(token)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in {401, 403}:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Auth service unavailable")
        except httpx.RequestError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Auth service unavailable")

    access_policy = _extract_access_policy(auth_me)
    profile = _extract_profile(payload, auth_me)
    project_id = _extract_project_id(auth_me)

    role = _resolve_role_from_policy(access_policy)
    if role is None:
        role = _resolve_role_from_profile(profile)

    if role is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User role is not authorized")

    return UserContext(
        sub=payload.get("sub", "unknown"),
        profile=profile,
        role=role,
        token=token,
        access_policy=access_policy,
        project_id=project_id,
    )


def require_roles(allowed_roles: Iterable[Role]):
    allowed = set(allowed_roles)

    async def _dependency(user: UserContext = Depends(get_user_context)) -> UserContext:
        if user.role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied for role")
        return user

    return _dependency
