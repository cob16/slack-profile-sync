import logging

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def update_status(
    token: str, status_text: str, status_emoji: str, status_expiration: int
):
    logging.debug("sending status update")
    client = WebClient(token=token)

    payload = dict(
        profile=dict(
            status_text=status_text,
            status_emoji=status_emoji,
            status_expiration=status_expiration,
        )
    )
    client.users_profile_set(**payload)


class AuthorisationGrantResponse:
    def __init__(self, success: bool, team=None, user=None, token=None, scope=None):
        self.success = success
        self.team = team
        self.user = user
        self.token = token
        self.scope = scope


def authorisation_grant(client_id, client_secret, code, redirect_uri):
    client = WebClient()

    try:
        response = client.oauth_v2_access(
            client_id=client_id,
            client_secret=client_secret,
            code=code,
            redirect_uri=redirect_uri,
        )
    except SlackApiError as e:
        logging.warning(e)
        logging.warning("returning success=False")
        return AuthorisationGrantResponse(success=False)

    return AuthorisationGrantResponse(
        success=True,
        team=response.data["team"]["id"],
        user=response.data["authed_user"]["id"],
        token=response.data["authed_user"]["access_token"],
        scope=response.data["authed_user"]["scope"],
    )
