import jwt
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

security = HTTPBearer()

def validate_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    # 1. Get Signing Key
    try:
        # Determine JWKS URL (fallback to base url + .well-known if not set)
        jwks_url = settings.MEDPLUM_JWKS_URL
        if not jwks_url:
            base = settings.MEDPLUM_BASE_URL
            if not base.endswith("/"):
                base += "/"
            jwks_url = f"{base}.well-known/jwks.json"

        jwks_client = jwt.PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
    except Exception as e:
        print(f"JWKS Error: {e}")
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
                "verify_nbf": True,
                "verify_iat": True,
                "verify_aud": True,
                "verify_iss": True,
                "require": ["exp", "iss", "aud", "nbf"], # Strictly require these claims
            },
            # Expected Values
            issuer=settings.MEDPLUM_JWT_ISSUER,
            audience=settings.MEDPLUM_JWT_AUDIENCE,
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidAudienceError:
        raise HTTPException(status_code=401, detail="Invalid audience")
    except jwt.InvalidIssuerError:
        raise HTTPException(status_code=401, detail="Invalid issuer")
    except Exception as e:
        print(f"JWT Decode Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
