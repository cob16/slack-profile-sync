import json
import logging

from slack_profile_update.handle_event import HandleEvent
from slack_profile_update.presenter.api_gateway_response import ApiGatewayResponse
from slack_profile_update.usecase.update_all_profiles import UpdateAllProfiles
from tests.test_helpers import event_signature_headers


def test_handle_user_change_event(test_file):
    event = test_file("example_user_updated_event.json")
    secret = "foobar"

    response = HandleEvent(
        environment={"SLACK_SIGNING_SECRET": secret},
        headers=event_signature_headers(secret, event),
        raw_body=event,
    ).execute()

    assert response.present() == ApiGatewayResponse().ok().present()


def test_logging_when_in_debug(caplog, test_file):
    event = test_file("example_user_updated_event.json")
    secret = "foobar"

    with caplog.at_level(logging.DEBUG):
        HandleEvent(
            environment={"SLACK_SIGNING_SECRET": secret},
            headers=event_signature_headers(secret, event),
            raw_body=event,
        ).execute()

    assert (
        "update event of user: 'me_devworkspace01' USERID: 'U019LN451HT' TEAMID: 'T019PQN3UAE' "
        "to status text: 'This is a test!' emoji ':smile:' expiration: '0'"
        in caplog.text
    ), "missing log entry"


def test_no_logging_when_not_in_debug(caplog, test_file):
    event = json.loads(test_file("example_user_updated_event.json"))

    with caplog.at_level(logging.INFO):
        UpdateAllProfiles(event).execute()

    assert caplog.text == "", "logs exist when they should not"
