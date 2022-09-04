import logging

import pytest

from slack_profile_update.gateway import slack as slack_gateway
from slack_profile_update.presenter.slack_user_link_model import SlackUserLinkModel


@pytest.mark.vcr
def test_can_call_update_status():
    slack_gateway.update_status(
        token="fake_api_token",
        status_text="This is a test!",
        status_emoji=":smile:",
        status_expiration=0,
    )


@pytest.mark.vcr
def test_authorisation_grant_when_code_invalid(caplog):
    with caplog.at_level(logging.WARNING):
        response = slack_gateway.authorisation_grant(
            client_id="foo", client_secret="bar", code="invalid-code", redirect_uri=None
        )

    assert response.success is False
    assert "returning success=False" in caplog.text, "missing log entry"
    assert "The server responded with: {'ok': False" in caplog.text, "missing log entry"


@pytest.mark.vcr
def test_authorisation_grant_on_success():
    response = slack_gateway.authorisation_grant(
        client_id="test-client-id",
        client_secret="test-client-secret",
        code="test-code",
        redirect_uri=None,
    )

    assert response.success == True
    assert response.team == "T019PQN3UAE"
    assert response.user == "U019LN451HT"
    assert response.token == "xoxp-123"
    assert response.scope == "users:read,users.profile:write"


@pytest.mark.vcr
def test_open_user_dialogue():
    response = slack_gateway.open_user_dialogue(
        token="fake_api_token", trigger_id="a-trigger-id", view={}
    )
    assert response
