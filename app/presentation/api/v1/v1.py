from fastapi import APIRouter
from .files import router as api_files


v1 = APIRouter()

v1.include_router(api_files, prefix="/files", tags=["files"])
