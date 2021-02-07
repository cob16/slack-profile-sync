from unittest import TestCase

import pytest

from slack_profile_update.presenter.api_gateway_response import (
    ApiGatewayResponse,
    NoResponseSetError,
)


class TestApiGatewayResponse(TestCase):
    def test_auth_error(self):
        response = ApiGatewayResponse().auth_error()

        assert response.present() == {
            "statusCode": 401,
            "headers": {},
            "body": None,
        }

    def test_ok(self):
        response = ApiGatewayResponse().ok()

        assert response.present() == {
            "statusCode": 204,
            "headers": {},
            "body": None,
        }

    def test_ok_with_body(self):
        body = dict(test="testing")
        response = ApiGatewayResponse().ok(body)

        assert response.present() == {
            "statusCode": 200,
            "headers": {},
            "body": '{"test": "testing"}',
        }

    def test_redirect(self):
        url = "https://example.com"
        response = ApiGatewayResponse().redirect(url=url)

        assert response.present() == {
            "statusCode": 307,
            "headers": {"Location": url},
            "body": None,
        }

    def test_throw_exception_if_response_not_set(self):
        response = ApiGatewayResponse()

        with pytest.raises(NoResponseSetError):
            response.present()
