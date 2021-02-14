from slack_profile_update.gateway.stub_user_token_store import StubUserTokenStore


def test_can_store_a_user_token():
    StubUserTokenStore().store("team", "user", "test-token")


def test_can_get_a_user_token():
    team_id = "team"
    user_id = "user"
    expected_token = "foobar"
    gateway = StubUserTokenStore()

    gateway.store(team_id, user_id, expected_token)

    token = gateway.fetch(team_id, user_id)

    assert expected_token == token
