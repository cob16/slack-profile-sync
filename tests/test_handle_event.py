import json
import logging

from slack_profile_update.gateway.stub_gateway import StubUserGateway
from slack_profile_update.handle_event import HandleEvent
from slack_profile_update.presenter.api_gateway_response import ApiGatewayResponse
from tests.test_helpers import event_signature_headers


def test_execute_returns_ok_if_event_not_found_error():
    secret = "some secret"
    event = "{}"
    with StubUserGateway().open() as stub_gateway:
        response = HandleEvent(
            environment={"SLACK_SIGNING_SECRET": secret},
            headers=event_signature_headers(secret, event),
            raw_body=event,
            user_store=stub_gateway,
        ).execute()

    # we do not want to error if the slack events api sends a event that is not supported
    assert response.present() == ApiGatewayResponse().ok().present()


def test_execute_returns_ok_if_event_callback_not_found_error(caplog):
    secret = "some secret"
    event = json.dumps(
        {
            "type": "event_callback",
            "event": {"type": "NOT SUPPORTED EVENT"},
        }
    )
    with StubUserGateway().open() as stub_gateway:
        with caplog.at_level(logging.ERROR):
            response = HandleEvent(
                environment={"SLACK_SIGNING_SECRET": secret},
                headers=event_signature_headers(secret, event),
                raw_body=event,
                user_store=stub_gateway,
            ).execute()

    assert f"unsupported event_callback" in caplog.text, "log does not exist"
    # we do not want to error if the slack events api sends a event that is not supported
    assert response.present() == ApiGatewayResponse().ok().present()


def test_execute_returns_ok_given_url_encoded_payload(caplog, test_file):
    # somtimes a payload will just be json.
    # other times such as for the shortcut interaction it will be wrapped in x-url-encoded under a payload param
    secret = "some secret"
    event = test_file("example_interaction_payload.x-url-encoded")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    headers.update(event_signature_headers(secret, event))

    with StubUserGateway().open() as stub_gateway:
        with caplog.at_level(logging.INFO):
            response = HandleEvent(
                environment={"SLACK_SIGNING_SECRET": secret},
                headers=headers,
                raw_body=event,
                user_store=stub_gateway,
            ).execute()

    assert f"shortcut event received" in caplog.text, "log does not exist"

    assert response.present() == ApiGatewayResponse().ok().present()
