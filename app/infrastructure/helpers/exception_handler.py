import enum
from typing import List

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.presentation.schemas.base_response import ResponseSchemaBase


class ExceptionType(enum.Enum):
    MS_UNAVAILABLE = 500, '990', 'Hệ thống đang bảo trì, quý khách vui lòng thử lại sau'
    MS_INVALID_API_PATH = 500, '991', 'Hệ thống đang bảo trì, quý khách vui lòng thử lại sau'
    DATA_RESPONSE_MALFORMED = 500, '992', 'Có lỗi xảy ra, vui lòng liên hệ admin!'


    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, http_code, code, message):
        self.http_code = http_code
        self.code = code
        self.message = message


class CustomException(Exception):
    http_code: int
    code: int
    message: str

    def __init__(self, http_code: int = None, code: int = None, message: str = None):
        self.http_code = http_code if http_code else 500
        self.code = code if code else self.http_code
        self.message = message

class AppException(Exception):
    def __init__(self, exception_type: ExceptionType, http_status: int = None, code: str = None,
                 message: str = None, formats: List[str] = None):
        if exception_type:
            if formats is not None:
                try:
                    exception_type.message = exception_type.message.format(*formats)
                except Exception as e:
                    print(e)
            self.http_status = exception_type.http_status
            self.code = exception_type.code
            self.message = exception_type.message
        else:
            self.http_status = http_status if http_status else 500
            self.code = code if code else str(self.http_status)
            self.message = message

    def __str__(self):
        return self.message


class ValidateException(AppException):

    def __init__(self, code: str = None, message: str = None):
        self.http_status = 400
        self.code = code if code else str(self.http_status)
        self.message = message


async def http_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.http_code,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(exc.code, exc.message))
    )


async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(400, get_message_validation(exc)))
    )


async def fastapi_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(500, "Có lỗi xảy ra, vui lòng liên hệ admin!"))
    )

async def request_validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(4, request_get_message_validation(exc)))
    )


def get_message_validation(exc):
    message = ""
    for error in exc.errors():
        message += "/'" + str(error.get("loc")[1]) + "'/" + ': ' + error.get("msg") + ", "

    message = message[:-2]

    return message

def request_get_message_validation(exc):
    print(exc.errors())
    messages = [error.get("loc")[len(error.get("loc")) - 1] for error in exc.errors()]
    return 'Trường dữ liệu không hợp lệ: {}'.format(', '.join(messages))