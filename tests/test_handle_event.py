import json
import logging

from slack_profile_update.handle_event import HandleEvent
from slack_profile_update.presenter.api_gateway_response import ApiGatewayResponse
from tests.test_helpers import event_signature_headers


def test_execute_returns_ok_if_event_not_found_error():
    secret = "some secret"
    event = "{}"
    response = HandleEvent(
        environment={"SLACK_SIGNING_SECRET": secret},
        headers=event_signature_headers(secret, event),
        raw_body=event,
    ).execute()

    # we do not want to error if the slack events api sends a event that is not supported
    assert response == ApiGatewayResponse().ok().present()


def test_execute_returns_ok_if_event_callback_not_found_error(caplog):
    secret = "some secret"
    event = json.dumps(
        {
            "type": "event_callback",
            "event": {"type": "NOT SUPPORTED EVENT"},
        }
    )
    with caplog.at_level(logging.ERROR):
        response = HandleEvent(
            environment={"SLACK_SIGNING_SECRET": secret},
            headers=event_signature_headers(secret, event),
            raw_body=event,
        ).execute()

    assert f"unsupported event_callback" in caplog.text, "log does not exist"
    # we do not want to error if the slack events api sends a event that is not supported
    assert response == ApiGatewayResponse().ok().present()
