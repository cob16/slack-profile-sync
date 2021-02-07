import json
from http import HTTPStatus


class NoResponseSetError(Exception):
    pass


class ApiGatewayResponse:
    def __init__(self):
        self.__status_code = None
        self.__headers = {}
        self.__body = None

    def auth_error(self):
        self.__status_code = HTTPStatus.UNAUTHORIZED.value
        return self

    def ok(self, body=None):
        if body is None:
            self.__status_code = HTTPStatus.NO_CONTENT.value
        else:
            self.__body = body
            self.__status_code = HTTPStatus.OK.value

        return self

    def redirect(self, url: str):
        self.__status_code = HTTPStatus.TEMPORARY_REDIRECT.value
        self.__headers = {"Location": url}
        return self

    def present(self):
        if self.__status_code is None:
            raise NoResponseSetError

        return {
            "statusCode": self.__status_code,
            "headers": self.__headers,
            "body": json.dumps(self.__body) if self.__body else None,
        }
