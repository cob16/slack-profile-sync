import json
from time import time

from slack_sdk.signature import SignatureVerifier

from slack_profile_update.handle_event import HandleEvent
from slack_profile_update.presenter.api_gateway_response import ApiGatewayResponse
from slack_profile_update.usecase.verify_request import VerifyRequest
from tests.test_helpers import event_signature_headers

signing_secret = "8f742231b10e8888abcd99yyyzzz85a5"
raw_body = "some_body"


def event_signature(signing_secret, timestamp, raw_body):
    return SignatureVerifier(signing_secret=signing_secret).generate_signature(
        timestamp=timestamp, body=raw_body
    )


def test_no_request_timestamp_header():
    assert (
        VerifyRequest(signing_secret=signing_secret).execute(
            raw_body,
            headers={
                "X-Slack-Signature": event_signature(
                    signing_secret, str(int(time())), raw_body
                )
            },
        )
        == False
    )


def test_no_request_signature_header():
    assert (
        VerifyRequest(signing_secret=signing_secret).execute(
            raw_body=raw_body,
            headers={
                "X-Slack-Request-Timestamp": str(int(time())),
            },
        )
        == False
    )


def test_verify_request_returns_true_if_timestamp_is_within_5_min():
    timestamp = int(time() - (60 * 3))
    headers = {
        "X-Slack-Signature": event_signature(signing_secret, timestamp, raw_body),
        "X-Slack-Request-Timestamp": str(timestamp),
    }

    assert (
        VerifyRequest(signing_secret=signing_secret).execute(raw_body, headers) == True
    )


def test_verify_request_returns_false_if_timestamp_is_more_than_5_min_old():
    headers = {
        "X-Slack-Request-Timestamp": str(int(time() - (time() - (60 * 6)))),
        "X-Slack-Signature": event_signature(signing_secret, int(time()), raw_body),
    }

    assert (
        VerifyRequest(signing_secret=signing_secret).execute(raw_body, headers) == False
    )


def test_verify_request_returns_false_if_timestamp_is_from_the_future():
    headers = {
        "X-Slack-Request-Timestamp": str(int(time() - (time() + 1))),
        "X-Slack-Signature": event_signature(signing_secret, int(time()), raw_body),
    }

    assert (
        VerifyRequest(signing_secret=signing_secret).execute(raw_body, headers) == False
    )


def test_verify_signature():
    raw_body = "foobar"
    headers = {
        "X-Slack-Request-Timestamp": str(int(time())),
        "X-Slack-Signature": event_signature(signing_secret, int(time()), raw_body),
    }

    assert (
        VerifyRequest(signing_secret=signing_secret).execute(raw_body, headers) == True
    )


def test_verify_signature_fails():
    raw_body = "foobar"
    headers = {
        "X-Slack-Request-Timestamp": str(int(time())),
        "X-Slack-Signature": event_signature("the wrong secret", int(time()), raw_body),
    }

    assert (
        VerifyRequest(signing_secret=signing_secret).execute(raw_body, headers) == False
    )

    headers = {
        "X-Slack-Request-Timestamp": str(int(time())),
        "X-Slack-Signature": event_signature(signing_secret, int(time()), "wrong body"),
    }

    assert (
        VerifyRequest(signing_secret=signing_secret).execute(raw_body, headers) == False
    )


def test_invalid_request_is_blocked():
    response = HandleEvent(
        environment={"SLACK_SIGNING_SECRET": "foo"},
        headers={},
        raw_body=json.dumps({"this is a test": "foobar"}),
    ).execute()

    assert response.present() == ApiGatewayResponse().auth_error().present()


def test_handle_url_verification_event(test_file):
    event = test_file("example_url_verification_event.json")
    secret = "foobar"

    response = HandleEvent(
        environment={"SLACK_SIGNING_SECRET": secret},
        headers=event_signature_headers(secret, event),
        raw_body=event,
    ).execute()

    expected_body = {
        "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P"
    }
    assert response.present() == ApiGatewayResponse().ok(expected_body).present()
