from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

STARVIT_PROTOCOL_CANONICAL_PREFIX = "urn:starvit:protocol-definition:"
STARVIT_PROTOCOL_IDENTIFIER_SYSTEM = "urn:starvit:protocol"
STARVIT_PROTOCOL_APPROVAL_REQUIRED_URL = "urn:starvit:protocol:approval-required"


class ProtocolStep(BaseModel):
    stepId: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    approvalRequired: bool = True


class ProtocolDefinitionSchema(BaseModel):
    protocolId: str = Field(..., min_length=1)
    version: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    status: str = Field("active")
    steps: List[ProtocolStep]

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        allowed = {"active", "draft", "retired"}
        if value not in allowed:
            raise ValueError("status must be active, draft, or retired")
        return value

    @model_validator(mode="after")
    def require_approval_steps(self) -> "ProtocolDefinitionSchema":
        if not any(step.approvalRequired for step in self.steps):
            raise ValueError("protocol definition must include at least one approval-required step")
        return self

    @property
    def canonical_url(self) -> str:
        return f"{STARVIT_PROTOCOL_CANONICAL_PREFIX}{self.protocolId}"


def build_protocol_definition_resource(schema: ProtocolDefinitionSchema) -> dict:
    actions = []
    for step in schema.steps:
        action = {
            "title": step.title,
            "description": step.description,
            "extension": [
                {
                    "url": STARVIT_PROTOCOL_APPROVAL_REQUIRED_URL,
                    "valueBoolean": step.approvalRequired,
                }
            ],
        }
        if step.stepId:
            action["id"] = step.stepId
        actions.append(action)

    return {
        "resourceType": "PlanDefinition",
        "url": schema.canonical_url,
        "identifier": [
            {
                "system": STARVIT_PROTOCOL_IDENTIFIER_SYSTEM,
                "value": schema.protocolId,
            }
        ],
        "version": schema.version,
        "status": schema.status,
        "title": schema.title,
        "action": actions,
    }
