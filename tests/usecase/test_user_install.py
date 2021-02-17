import logging

from slack_profile_update.domain.user import User
from slack_profile_update.gateway import slack
from slack_profile_update.gateway.slack import AuthorisationGrantResponse
from slack_profile_update.gateway.stub_user_token_store import StubUserTokenStore
from slack_profile_update.handle_request import HandleRequest
from slack_profile_update.usecase.user_install import UserInstall
from tests.test_handle_request import example_request


def test_user_install_stores_token_if_success(mocker):
    expected_user = User(team_id="foo-team", user_id="foo-user")
    mocker.patch(
        "slack_profile_update.gateway.slack.authorisation_grant",
        return_value=AuthorisationGrantResponse(
            success=True,
            team=expected_user.team_id,
            user=expected_user.user_id,
            token="foo-token",
        ),
    )
    client_id = "test client id"
    client_secret = "test client secret"
    stub_user_token_store = StubUserTokenStore()
    user_install = UserInstall(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="example.com",
        user_token_store=stub_user_token_store,
    )
    response = user_install.execute("foobar", "test-state")
    assert response.present()["statusCode"] == 200

    assert stub_user_token_store.fetch(expected_user).token == "foo-token"


def test_user_install(caplog, mocker):
    mocker.patch(
        "slack_profile_update.gateway.slack.authorisation_grant",
        return_value=AuthorisationGrantResponse(
            True, "foo-team", "foo-user", "foo-token"
        ),
    )
    client_id = "test client id"
    client_secret = "test client secret"
    with caplog.at_level(logging.DEBUG):
        response = HandleRequest().execute(
            {
                "SLACK_SIGNING_SECRET": "is_secret",
                "CLIENT_ID": client_id,
                "CLIENT_SECRET": client_secret,
                "REDIRECT_URI": "example.com",
            },
            example_request(
                headers=None,
                http_method="GET",
                path="/oauth/authorization_grant",
                query_arguments={
                    "code": ["foobar"],
                    "state": ["test-state"],
                },
            ),
        )

    slack.authorisation_grant.assert_called_once_with(
        client_id=client_id,
        client_secret=client_secret,
        code="foobar",
        redirect_uri="example.com",
    )

    assert response["statusCode"] == 200
    assert "Thank you!" in response["body"]

    assert "received authorization_grant code" in caplog.text, "missing log entry"


def test_user_install_missing_code(caplog):
    secret = "is_secret"
    with caplog.at_level(logging.DEBUG):
        response = HandleRequest().execute(
            {
                "SLACK_SIGNING_SECRET": secret,
                "CLIENT_ID": "bar",
                "CLIENT_SECRET": "foo",
            },
            example_request(
                headers=None,
                http_method="GET",
                path="/oauth/authorization_grant",
                query_arguments={
                    "state": ["test-state"],
                },
            ),
        )

    assert response["statusCode"] == 404
    assert response["body"] is None

    assert "missing code or state" in caplog.text


def test_user_install_missing_sate(caplog):
    secret = "is_secret"
    with caplog.at_level(logging.DEBUG):
        response = HandleRequest().execute(
            {
                "SLACK_SIGNING_SECRET": secret,
                "CLIENT_ID": "bar",
                "CLIENT_SECRET": "foo",
                "REDIRECT_URI": "example.com",
            },
            example_request(
                headers=None,
                http_method="GET",
                path="/oauth/authorization_grant",
                query_arguments={"code": ["foobar"]},
            ),
        )

    assert response["statusCode"] == 404
    assert response["body"] is None

    assert "missing code or state" in caplog.text


def test_user_install_returns_failure(caplog, mocker):
    mocker.patch(
        "slack_profile_update.gateway.slack.authorisation_grant",
        return_value=AuthorisationGrantResponse(success=False),
    )
    slack_signing_secret = "is_secret"
    client_id = "test client id"
    client_secret = "test client secret"
    redirect_uri = "test-redirect-url.com"
    with caplog.at_level(logging.DEBUG):
        response = HandleRequest().execute(
            {
                "SLACK_SIGNING_SECRET": slack_signing_secret,
                "CLIENT_ID": client_id,
                "CLIENT_SECRET": client_secret,
                "REDIRECT_URI": redirect_uri,
            },
            example_request(
                headers=None,
                http_method="GET",
                path="/oauth/authorization_grant",
                query_arguments={
                    "code": ["foobar"],
                    "state": ["test-state"],
                },
            ),
        )

    slack.authorisation_grant.assert_called_once_with(
        client_id=client_id,
        client_secret=client_secret,
        code="foobar",
        redirect_uri=redirect_uri,
    )

    assert response["statusCode"] == 401
    assert response["body"] is None

    assert (
        "returning auth error due to gateway failure" in caplog.text
    ), "missing log entry"
