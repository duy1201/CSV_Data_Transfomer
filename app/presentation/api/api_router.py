from fastapi import APIRouter
from app.presentation.api import auth
from app.presentation.api.v1 import v1

router = APIRouter()

router.include_router(auth.router, tags=["login"])
router.include_router(v1, prefix='/v1',  tags=["v1"])

