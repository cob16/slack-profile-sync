import logging

from slack_sdk.oauth import RedirectUriPageRenderer


class UserInstall:
    def execute(self, code, state):
        logging.debug(
            "received authorization_grant code '%s'",
            code,
        )
        logging.debug(
            "received authorization_grant state '%s'",
            state,
        )
        body = RedirectUriPageRenderer(
            install_path="", redirect_uri_path=""
        ).render_success_page(app_id="fakeappid", team_id=None)
        return body
