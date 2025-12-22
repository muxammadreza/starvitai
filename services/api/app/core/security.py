import jwt
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

import logging

logger = logging.getLogger("starvit-auth")

# Global JWK Client to avoid re-fetching on every request
_jwks_client = None

def get_jwks_client():
    global _jwks_client
    if _jwks_client is None:
        jwks_url = settings.JWKS_URL
        if not jwks_url:
            raise RuntimeError("JWKS_URL is not configured")
        _jwks_client = jwt.PyJWKClient(jwks_url)
    return _jwks_client

security = HTTPBearer()

def validate_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    # 1. Get Signing Key
    try:
        jwks_client = get_jwks_client()
        signing_key = jwks_client.get_signing_key_from_jwt(token)
    except Exception as e:
        logger.error(f"JWKS Error: {e}")
        raise HTTPException(status_code=401, detail="Could not retrieve signing key")

    # 2. Verify Token
    try:
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            # Verification Settings
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iat": True,
                "verify_aud": True,
                "verify_iss": True,
                "require": ["exp", "iss", "aud"],
            },
            # Expected Values from Settings
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE,
        )
        payload["_token"] = token
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidAudienceError:
        raise HTTPException(status_code=401, detail="Invalid audience")
    except jwt.InvalidIssuerError:
        raise HTTPException(status_code=401, detail="Invalid issuer")
    except Exception as e:
        logger.error(f"JWT Decode Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
