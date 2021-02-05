import json
from slack_profile_update.handle_event import HandleEvent


def test_invalid_request_is_blocked():
    response = HandleEvent(
        environment={"SLACK_SIGNING_SECRET": "foo"},
        headers={},
        raw_body=json.dumps({"this is a test": "foobar"}),
    ).execute()

    assert response == "{}"


def test_handle_url_verification_event(test_file, create_signature_headers):
    event = test_file("example_url_verification_event.json")
    secret = "foobar"

    response = HandleEvent(
        environment={"SLACK_SIGNING_SECRET": secret},
        headers=create_signature_headers(secret, event),
        raw_body=event,
    ).execute()

    assert (
        response
        == '{"challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P"}'
    )
