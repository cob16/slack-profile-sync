import json
import logging

import pytest

from slack_profile_update.domain.slackuser import SlackUser
from slack_profile_update.gateway.stub_gateway import StubUserGateway
from slack_profile_update.handle_event import HandleEvent
from slack_profile_update.usecase.user_uninstall import UserUninstall
from tests.test_helpers import event_signature_headers


def test_user_uninstall_removed_users_from_gateways(test_file):
    event = test_file("user_token_revoked.json")
    secret = "secret"

    user_to_be_removed = SlackUser("U019LN451HT", "T019PQN3UAE", "token1")
    linked_user_1 = SlackUser("user1", "team1", "token2")
    linked_user_2 = SlackUser("user2", "team1", "token3")

    with StubUserGateway().open() as user_store:

        user_app_id = user_store.create_app_user()
        user_store.create_slack_user(user_to_be_removed, user_app_id)
        user_store.create_slack_user(linked_user_1, user_app_id)
        user_store.create_slack_user(linked_user_2, user_app_id)

        response = HandleEvent(
            environment={"SLACK_SIGNING_SECRET": secret},
            headers=event_signature_headers(secret, event),
            raw_body=event,
            user_store=user_store,
        ).execute()

        assert response.present() == {
            "statusCode": 204,
            "headers": {},
            "body": None,
        }

        users = user_store.get_slack_users(app_user_id=user_app_id)
        assert linked_user_1 in users
        assert linked_user_2 in users
        assert user_to_be_removed not in users
        assert len(users) == 2


def test_user_uninstall_logs_message(caplog, test_file):
    event = json.loads(test_file("user_token_revoked.json"))

    user_to_be_removed = SlackUser("U019LN451HT", "T019PQN3UAE", "token1")
    with StubUserGateway().open() as user_store:
        app_user_id = user_store.create_app_user()
        user_store.create_slack_user(user_to_be_removed, app_user_id)

        with caplog.at_level(logging.INFO):
            UserUninstall(user_store=user_store).execute(event)

        assert "uninstalled user" in caplog.text, "missing log entry"


def test_user_uninstall_with_no_exsisting_user(caplog, test_file):
    event = json.loads(test_file("user_token_revoked.json"))

    with caplog.at_level(logging.WARNING):
        with StubUserGateway().open() as stub_gateway:
            UserUninstall(user_store=stub_gateway).execute(event)

    assert "tried to uninstall user that did not exist" in caplog.text
