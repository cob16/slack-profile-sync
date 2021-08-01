import logging

from slack_sdk.oauth import RedirectUriPageRenderer

from slack_profile_update.domain.slackuser import SlackUser
from slack_profile_update.gateway import slack
from slack_profile_update.presenter.api_gateway_response import ApiGatewayResponse

EXPECTED_SCOPE = "users:read,users.profile:write"


class UserInstall:
    def __init__(self, client_id, client_secret, redirect_uri, user_token_store):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__redirect_uri = redirect_uri
        self.__user_token_store = user_token_store

    def execute(self, code, state):
        logging.debug(
            "received authorization_grant code '%s'",
            code,
        )
        logging.debug(
            "received authorization_grant state '%s'",
            state,
        )
        gateway_response = slack.authorisation_grant(
            client_id=self.__client_id,
            client_secret=self.__client_secret,
            code=code,
            redirect_uri=self.__redirect_uri,
        )
        response = ApiGatewayResponse()
        if not gateway_response.success:
            logging.warning("returning auth error due to gateway failure")
            return response.auth_error()

        if gateway_response.scope == EXPECTED_SCOPE:
            body = RedirectUriPageRenderer(
                install_path="", redirect_uri_path=""
            ).render_success_page(app_id="fakeappid", team_id=None)
            user = SlackUser(
                team_id=gateway_response.team,
                user_id=gateway_response.user,
                token=gateway_response.token,
            )
            self.__user_token_store.store(user)
            return response.ok_html(body)
        else:
            logging.warning(
                f"scope differs from expected scope {gateway_response.scope} != {EXPECTED_SCOPE}"
            )
            return response.auth_error()
