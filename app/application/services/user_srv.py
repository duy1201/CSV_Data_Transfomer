from datetime import datetime
from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

from app.infrastructure.core.config import settings


class UserService:
    def __init__(self):
        pass

    reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )

    @staticmethod
    def authenticate(username: str, password: str) -> Optional[int]:
        if username != settings.ADMIN_USERNAME and password != settings.ADMIN_PASSWORD:
            return None
        return settings.ADMIN_ID

    @staticmethod
    def get_current_user(http_authorization_credentials=Depends(reusable_oauth2)) -> int:
        try:
            payload = jwt.decode(
                http_authorization_credentials.credentials, settings.SECRET_KEY, algorithms=[settings.SECURITY_ALGORITHM]
            )
            if payload.get("exp") < datetime.now().timestamp():
                raise HTTPException(status_code=403, detail="Token expired")
            if payload["user_id"] != str(settings.ADMIN_ID):
                raise HTTPException(status_code=404, detail="User not found")
            return payload["user_id"]
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=403,
                detail=f"Could not validate credentials",
            )


