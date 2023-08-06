from typing import Optional


class APIException(Exception):
    status_code: int = 500
    default_code: str = 'server_error'
    default_detail: str = 'Server Error.'
    error_detail: Optional[dict] = None

    def __init__(
        self,
        error_detail: Optional[dict] = None,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
    ):
        super().__init__()
        if status_code:
            self.status_code = status_code

        self.error_code = error_code if error_code else self.default_code

        self.error_detail = (
            error_detail
            if error_detail
            else self.error_detail
            or {'error_code': self.error_code, 'detail': self.default_detail}
        )

    def __str__(self) -> str:
        return f'Status code: {self.status_code}, error_code: {self.error_code}, detail: {self.error_detail}'

    def response(self) -> dict:
        return self.error_detail


class PermissionDenied(APIException):
    status: int = 403
    error_detail: dict = {
        'status': 'error',
        'message': 'you have no permissions for this endpoint.',
    }


class InvalidDateParams(APIException):
    status_code = 422
    default_code = 'invalid_date'
    default_detail = 'Invalid date params.'


class ReportUpdating(APIException):
    status_code = 204


class DontHaveReportData(APIException):
    status_code = 406
    default_detail = 'Dont have reports for this integration'


class InvalidFieldsParam(APIException):
    status_code = 422
    default_code = 'invalid_fields'
    default_detail = 'Invalid fields param, fields must be a list'


class NotDataException(APIException):
    status_code = 400
    default_code = 'no data'
    default_detail = 'no data ever'
