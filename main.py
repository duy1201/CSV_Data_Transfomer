# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
# from sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.infrastructure.database.base import engine
from app.infrastructure.models import Base
from app.presentation.api.api_router import router
# from app.models import Base
# from app.db.base import engine
from app.infrastructure.core.config import settings
from app.infrastructure.helpers.exception_handler import CustomException, http_exception_handler, \
    validation_exception_handler, fastapi_error_handler

# logging.config.fileConfig(settings.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
Base.metadata.create_all(bind=engine)


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, docs_url="/docs", redoc_url='/re-docs',
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        description='''
        Base frame with FastAPI micro framework + Postgresql
            - Login/Register with JWT
            - Permission
            - CRUD User
            - Unit testing with Pytest
            - Dockerize
        '''
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(router, prefix=settings.API_PREFIX)
    application.add_exception_handler(CustomException, http_exception_handler)
    application.add_exception_handler(ValidationError, validation_exception_handler)
    application.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    application.add_exception_handler(Exception, fastapi_error_handler)


    return application


app = get_application()
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
