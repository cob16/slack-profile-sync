from unittest import TestCase

from slack_profile_update.handle_request import HandleRequest
from tests.test_helpers import event_signature_headers


def test_event_routing():
    secret = "is_secret"
    some_data = "{}"
    response = HandleRequest().execute(
        {"SLACK_SIGNING_SECRET": secret},
        example_request(
            headers=event_signature_headers(secret, some_data),
            http_method="POST",
            body=some_data,
        ),
    )
    assert response["statusCode"] == 204


def test_get_returns_404_unknown_path():
    secret = "is_secret"
    response = HandleRequest().execute(
        {"SLACK_SIGNING_SECRET": secret},
        example_request(headers=None, http_method="GET", path="/some/random/path"),
    )
    assert response["statusCode"] == 404


def example_request(
    http_method, headers=None, query_arguments=None, path="/foo/path", body=None
):
    if query_arguments is None:
        query_arguments = {}
    if headers is None:
        headers = {}
    return {
        "input": {
            "path": path,
            "requestContext": {
                "httpMethod": http_method,
            },
            "headers": headers,
            "multiValueQueryStringParameters": query_arguments,
            "body": body,
        },
    }
