import pytest

from slack_profile_update.domain.slackuser import SlackUser
from slack_profile_update.gateway.stub_user_token_store import StubUserTokenStore


def test_can_store_a_user_token():
    StubUserTokenStore().store(SlackUser("team", "user", "test-token"))


def test_can_get_a_user_token():
    team_id = "team"
    user_id = "user"
    expected_token = "foobar"
    gateway = StubUserTokenStore()

    expected_user = SlackUser(user_id=user_id, team_id=team_id, token=expected_token)
    gateway.store(expected_user)

    user = gateway.fetch(expected_user)

    assert expected_user == user
    assert expected_token == user.token


def test_remove_a_user_token():
    team_id = "team"
    user_id = "user"
    expected_token = "foobar"
    gateway = StubUserTokenStore()
    expected_user = SlackUser(user_id=user_id, team_id=team_id, token=expected_token)
    gateway.store(expected_user)
    gateway.fetch(expected_user)

    assert gateway.remove(expected_user) is True

    with pytest.raises(KeyError):
        gateway.fetch(expected_user)


def test_remove_non_existent_is_silent():
    team_id = "team"
    user_id = "user"
    expected_token = "foobar"
    gateway = StubUserTokenStore()
    expected_user = SlackUser(user_id=user_id, team_id=team_id, token=expected_token)
    unstored_user = SlackUser(user_id="foo", team_id="bar", token=None)

    gateway.store(expected_user)

    assert gateway.remove(unstored_user) is False
