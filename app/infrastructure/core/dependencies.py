from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.services.file_srv import FileService
from app.infrastructure.data_processor import DataProcessor
from app.infrastructure.database.base import get_db_session
from app.application.services.user_srv import UserService
from app.infrastructure.repositories.file_repo import FileRepository


def login_required(http_authorization_credentials=Depends(UserService().reusable_oauth2)):
    return UserService().get_current_user(http_authorization_credentials)

def get_file_service(session: Session = Depends(get_db_session)) -> FileService:
    return FileService(FileRepository(session), DataProcessor(), "./uploads")