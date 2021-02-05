from time import time

from slack_profile_update.usecase.verify_request import VerifyRequest

signing_secret = "8f742231b10e8888abcd99yyyzzz85a5"
raw_body = "some_body"


def test_no_request_timestamp_header(create_signature):
    assert (
        VerifyRequest(signing_secret=signing_secret).execute(
            raw_body,
            headers={
                "X-Slack-Signature": create_signature(
                    signing_secret, int(time()), raw_body
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


def test_verify_request_returns_true_if_timestamp_is_within_5_min(create_signature):
    timestamp = int(time() - (60 * 3))
    headers = {
        "X-Slack-Signature": create_signature(signing_secret, timestamp, raw_body),
        "X-Slack-Request-Timestamp": str(timestamp),
    }

    assert (
        VerifyRequest(signing_secret=signing_secret).execute(raw_body, headers) == True
    )


def test_verify_request_returns_false_if_timestamp_is_more_than_5_min_old(
    create_signature,
):
    headers = {
        "X-Slack-Request-Timestamp": str(int(time() - (time() - (60 * 6)))),
        "X-Slack-Signature": create_signature(signing_secret, int(time()), raw_body),
    }

    assert (
        VerifyRequest(signing_secret=signing_secret).execute(raw_body, headers) == False
    )


def test_verify_request_returns_false_if_timestamp_is_from_the_future(create_signature):
    headers = {
        "X-Slack-Request-Timestamp": str(int(time() - (time() + 1))),
        "X-Slack-Signature": create_signature(signing_secret, int(time()), raw_body),
    }

    assert (
        VerifyRequest(signing_secret=signing_secret).execute(raw_body, headers) == False
    )


def test_verify_signature(create_signature):
    raw_body = "foobar"
    headers = {
        "X-Slack-Request-Timestamp": str(int(time())),
        "X-Slack-Signature": create_signature(signing_secret, int(time()), raw_body),
    }

    assert (
        VerifyRequest(signing_secret=signing_secret).execute(raw_body, headers) == True
    )


def test_verify_signature_fails(create_signature):
    raw_body = "foobar"
    headers = {
        "X-Slack-Request-Timestamp": str(int(time())),
        "X-Slack-Signature": create_signature(
            "the wrong secret", int(time()), raw_body
        ),
    }

    assert (
        VerifyRequest(signing_secret=signing_secret).execute(raw_body, headers) == False
    )

    headers = {
        "X-Slack-Request-Timestamp": str(int(time())),
        "X-Slack-Signature": create_signature(
            signing_secret, int(time()), "wrong body"
        ),
    }

    assert (
        VerifyRequest(signing_secret=signing_secret).execute(raw_body, headers) == False
    )
