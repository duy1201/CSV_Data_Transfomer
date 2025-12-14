from typing import TypeVar, Generic, Optional
from pydantic import BaseModel
from pydantic.v1.generics import GenericModel

T = TypeVar('T')


class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: int = 200
    message: str = 'OK'

    def custom_response(self, code: int, message: str):
        self.code = code
        self.message = message
        return self

    def success_response(self):
        self.code = 200
        self.message = 'OK'
        return self


class BaseResponse(ResponseSchemaBase):

    def success(self) -> 'BaseResponse':
        return self


class DataResponse(ResponseSchemaBase, Generic[T]):
    data: Optional[T] = None

    def success_response(self, data: Optional[T] = None):
        self.code = 200
        self.message = 'OK'
        self.data = data
        return self

    def fail_response(self, code: int, message: str, data: Optional[T] = None):
        self.code = code
        self.message = message
        self.data = data
        return self
