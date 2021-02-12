import logging

from slack_sdk.oauth import RedirectUriPageRenderer

from slack_profile_update.gateway import slack
from slack_profile_update.presenter.api_gateway_response import ApiGatewayResponse


class UserInstall:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

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
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code,
            redirect_uri="example.com",
        )
        response = ApiGatewayResponse()
        if gateway_response.success:
            body = RedirectUriPageRenderer(
                install_path="", redirect_uri_path=""
            ).render_success_page(app_id="fakeappid", team_id=None)
            return response.ok_html(body)
        else:
            logging.warning("returning auth error due to gateway failure")
            return response.auth_error()
