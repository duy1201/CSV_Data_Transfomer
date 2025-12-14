from fastapi import APIRouter, Depends, UploadFile, File, Query
from typing import List, Optional
from datetime import date

from app.application.services.file_srv import FileService
from app.infrastructure.core.dependencies import get_file_service, login_required
from app.infrastructure.helpers.exception_handler import CustomException
from app.presentation.schemas.base_response import DataResponse
from app.presentation.schemas.files import FileMetadataResponse, TransactionResponse, SummaryResponse

router = APIRouter()


@router.post("/upload", dependencies=[Depends(login_required)], response_model=DataResponse[FileMetadataResponse])
def upload_file(file: UploadFile = File(...), service: FileService = Depends(get_file_service)):
    try:
        return DataResponse().success_response(data=service.upload_file(file))
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.get("", response_model=DataResponse[List[FileMetadataResponse]])
def list_files(service: FileService = Depends(get_file_service)):
    try:
        return DataResponse().success_response(service.get_all_files())
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.get("/{file_id}/transactions", dependencies=[Depends(login_required)], response_model=DataResponse[List[TransactionResponse]])
async def list_transactions(
        file_id: str,
        category: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        page: int = Query(1, ge=1), page_size: int = Query(20, le=100),
        service: FileService = Depends(get_file_service)
):
    try:
        return DataResponse().success_response(data=
            service.get_transactions(file_id, page, page_size, category, date_from, date_to)
        )
    except Exception as e:
        raise CustomException(http_code=400, code=400, message=str(e))


@router.get("/{file_id}/summary",dependencies=[Depends(login_required)], response_model=DataResponse[SummaryResponse])
async def get_summary(file_id: str, service: FileService = Depends(get_file_service)):
    try:
        return DataResponse().success_response(data=service.get_file_summary(file_id))
    except Exception as e:
        raise CustomException(http_code=400, code=400, message=str(e))
