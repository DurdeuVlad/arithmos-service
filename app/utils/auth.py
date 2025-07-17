import os
from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

# 1. Define your settings model for fastapi-jwt-auth
class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-me")

# 2. Tell AuthJWT how to load your config
@AuthJWT.load_config
def get_config() -> Settings:
    return Settings()

# 3. The actual dependency that your routes will use
async def get_current_user(Authorize: AuthJWT = Depends()):
    """
    Dependency to extract and verify JWT token, raising 401 if invalid.
    """
    try:
        Authorize.jwt_required()
        user = Authorize.get_jwt_subject()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token: no subject")
        return user
    except Exception as e:
        # return the original JWT-Auth error message
        raise HTTPException(status_code=401, detail=str(e))
