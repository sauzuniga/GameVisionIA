from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from jwt import PyJWKClient
import os
from dotenv import load_dotenv

load_dotenv()

JWKS_URL = "https://czvvyuinrfgsvcyzlgqu.supabase.co/auth/v1/.well-known/jwks.json"
jwks_client = PyJWKClient(JWKS_URL)
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    token = credentials.credentials
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["ES256"],
            audience="authenticated"
        )
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Sesión expirada")
    except jwt.InvalidTokenError as e:
        print(f"JWT Error: {e}")
        raise HTTPException(status_code=401, detail="Token inválido")