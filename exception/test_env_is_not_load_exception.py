from exception.base_exception import BaseException


class TestEnvIsNotLoadException(BaseException):
    status_code = 400
    detail = "Required testing enviroment"
