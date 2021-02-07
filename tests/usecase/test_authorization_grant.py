import logging

from slack_profile_update.handle_request import HandleRequest
from tests.test_handle_request import example_request


def test_authorization_grant(caplog):
    secret = "is_secret"
    with caplog.at_level(logging.DEBUG):
        response = HandleRequest().execute(
            {"SLACK_SIGNING_SECRET": secret},
            example_request(
                headers=None,
                http_method="GET",
                path="/oauth/authorization_grant",
                query_arguments={
                    "code": ["foobar"],
                    "state": ["test-state"],
                },
            ),
        )

    assert response["statusCode"] == 200
    assert response["body"] is not None

    assert "received authorization_grant code" in caplog.text, "missing log entry"


def test_authorization_grant_missing_code(caplog):
    secret = "is_secret"
    with caplog.at_level(logging.DEBUG):
        response = HandleRequest().execute(
            {"SLACK_SIGNING_SECRET": secret},
            example_request(
                headers=None,
                http_method="GET",
                path="/oauth/authorization_grant",
                query_arguments={
                    "state": ["test-state"],
                },
            ),
        )

    assert response["statusCode"] == 404
    assert response["body"] is None

    assert caplog.text == ""


def test_authorization_grant_missing_sate(caplog):
    secret = "is_secret"
    with caplog.at_level(logging.DEBUG):
        response = HandleRequest().execute(
            {"SLACK_SIGNING_SECRET": secret},
            example_request(
                headers=None,
                http_method="GET",
                path="/oauth/authorization_grant",
                query_arguments={"code": ["foobar"]},
            ),
        )

    assert response["statusCode"] == 404
    assert response["body"] is None

    assert caplog.text == ""
