from fastapi import APIRouter, HTTPException

from app.infrastructure.core.security import create_access_token
from app.presentation.schemas.auth import LoginRequest
from app.presentation.schemas.base_response import DataResponse
from app.application.services.user_srv import UserService

router = APIRouter()

@router.post('/auth/token')
def login_access_token(login_info:LoginRequest):
    user_id = UserService.authenticate(login_info.username, login_info.password)
    if not user_id:
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    return DataResponse().success_response({
        'access_token': create_access_token(user_id=user_id)
    })
