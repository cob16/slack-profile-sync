import json
import logging
from unittest.mock import call

from slack_profile_update.domain.slackuser import SlackUser
from slack_profile_update.gateway import slack
from slack_profile_update.gateway.stub_gateway import StubUserGateway
from slack_profile_update.handle_event import HandleEvent
from slack_profile_update.presenter.api_gateway_response import ApiGatewayResponse
from slack_profile_update.usecase.update_all_profiles import UpdateAllProfiles
from tests.test_helpers import event_signature_headers


def test_handle_user_change_event(test_file):
    event = test_file("example_user_updated_event.json")
    secret = "foobar"

    with StubUserGateway().open() as user_store:
        response = HandleEvent(
            environment={"SLACK_SIGNING_SECRET": secret},
            headers=event_signature_headers(secret, event),
            raw_body=event,
            user_store=user_store,
        ).execute()

    assert response.present() == ApiGatewayResponse().ok().present()


def test_logging_when_in_debug(caplog, test_file):
    event = test_file("example_user_updated_event.json")
    secret = "foobar"

    with StubUserGateway().open() as user_store:
        with caplog.at_level(logging.DEBUG):
            HandleEvent(
                environment={"SLACK_SIGNING_SECRET": secret},
                headers=event_signature_headers(secret, event),
                raw_body=event,
                user_store=user_store,
            ).execute()

        assert (
            "update event of user: 'me_devworkspace01' USERID: 'U019LN451HT' TEAMID: 'T019PQN3UAE' "
            "to status text: 'This is a test!' emoji ':smile:' expiration: '0'"
            in caplog.text
        ), "missing log entry"


def test_updates_status_of_linked_users(caplog, test_file, mocker):
    mocker.patch(
        "slack_profile_update.gateway.slack.update_status",
        return_value=True,
    )
    event = json.loads(test_file("example_user_updated_event.json"))

    source_user = SlackUser("U019LN451HT", "T019PQN3UAE", "token1")
    dest_user_1 = SlackUser("user1", "team1", "token2")
    dest_user_2 = SlackUser("user3", "team3", "token3")

    with StubUserGateway().open() as user_store:
        app_user_id = user_store.create_app_user()
        user_store.create_slack_user(source_user, app_user_id)
        user_store.create_slack_user(dest_user_1, app_user_id)
        user_store.create_slack_user(dest_user_2, app_user_id)

        UpdateAllProfiles(user_store=user_store).execute(event)

    slack.update_status.assert_has_calls(
        [
            call(
                status_emoji=":smile:",
                status_expiration=0,
                status_text="This is a test!",
                token=dest_user_1.token,
            ),
            call(
                status_emoji=":smile:",
                status_expiration=0,
                status_text="This is a test!",
                token=dest_user_2.token,
            ),
        ],
        any_order=True,
    )
