from slack_profile_update.domain.user import User
from slack_profile_update.gateway.stub_user_token_store import StubUserTokenStore


def test_can_store_a_user_token():
    StubUserTokenStore().store(User("team", "user", "test-token"))


def test_can_get_a_user_token():
    team_id = "team"
    user_id = "user"
    expected_token = "foobar"
    gateway = StubUserTokenStore()

    expected_user = User(user_id=user_id, team_id=team_id, token=expected_token)
    gateway.store(expected_user)

    user = gateway.fetch(expected_user)

    assert expected_user == user
    assert expected_token == user.token
