import json
import logging

import pytest

from slack_profile_update.domain.user import User
from slack_profile_update.gateway.stub_user_link_store import StubUserLinkStore
from slack_profile_update.gateway.stub_user_token_store import StubUserTokenStore
from slack_profile_update.handle_event import HandleEvent
from slack_profile_update.usecase.user_uninstall import UserUninstall
from tests.test_helpers import event_signature_headers


def test_user_uninstall_removed_users_from_gateways(test_file):
    event = test_file("user_token_revoked.json")
    secret = "secret"

    user_to_be_removed = User("U019LN451HT", "T019PQN3UAE", "token1")
    linked_user_1 = User("user1", "team1", "token2")
    linked_user_2 = User("user2", "team1", "token3")

    link_store = StubUserLinkStore()
    link_store.link(user_to_be_removed, linked_user_1)
    link_store.link(user_to_be_removed, linked_user_2)

    token_store = StubUserTokenStore()
    token_store.store(user_to_be_removed)
    token_store.store(linked_user_1)
    token_store.store(linked_user_2)

    response = HandleEvent(
        environment={"SLACK_SIGNING_SECRET": secret},
        headers=event_signature_headers(secret, event),
        raw_body=event,
        user_link_store=link_store,
        user_token_store=token_store,
    ).execute()

    assert response.present() == {
        "statusCode": 204,
        "headers": {},
        "body": None,
    }

    with pytest.raises(KeyError):
        token_store.fetch(user_to_be_removed)
    with pytest.raises(KeyError):
        link_store.fetch(user_to_be_removed)

    # does not remove linked users
    token_store.fetch(linked_user_1)
    token_store.fetch(linked_user_2)
    link_store.fetch(linked_user_2)
    link_store.fetch(linked_user_2)


def test_user_uninstall_logs_message(caplog, test_file):
    event = json.loads(test_file("user_token_revoked.json"))

    user_to_be_removed = User("U019LN451HT", "T019PQN3UAE", "token1")
    token_store = StubUserTokenStore()
    token_store.store(user_to_be_removed)

    with caplog.at_level(logging.INFO):
        UserUninstall(
            user_link_store=StubUserLinkStore(), user_token_store=token_store
        ).execute(event)

    assert "uninstalled user" in caplog.text, "missing log entry"


def test_user_uninstall_with_no_exsisting_user(caplog, test_file):
    event = json.loads(test_file("user_token_revoked.json"))

    with caplog.at_level(logging.WARNING):
        UserUninstall(
            user_link_store=StubUserLinkStore(), user_token_store=StubUserTokenStore()
        ).execute(event)

    assert "tried to uninstall user that did not exist" in caplog.text
