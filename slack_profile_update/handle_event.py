import json
import logging
from urllib.parse import parse_qs

from slack_profile_update.presenter.api_gateway_response import ApiGatewayResponse
from slack_profile_update.usecase.update_all_profiles import UpdateAllProfiles
from slack_profile_update.usecase.url_verification import UrlVerification
from slack_profile_update.usecase.user_uninstall import UserUninstall
from slack_profile_update.usecase.verify_request import VerifyRequest


class HandleEvent:
    def __init__(
        self,
        environment,
        headers,
        raw_body,
        user_store,
    ):
        self.raw_body = raw_body
        self.headers = headers
        self.signing_secret = environment["SLACK_SIGNING_SECRET"]
        self.user_store = user_store

    def execute(self):
        response = ApiGatewayResponse()
        if not VerifyRequest(signing_secret=self.signing_secret).execute(
            self.raw_body, self.headers
        ):
            response.auth_error()
            return response

        if self.headers.get("Content-Type") == "application/x-www-form-urlencoded":
            self.raw_body = parse_qs(self.raw_body).get("payload")[0]

        body = json.loads(self.raw_body)
        logging.debug(body)

        type = body.get("type")
        if type == "url_verification":
            response_body = UrlVerification().execute(body)
            response.ok(response_body)
        elif type == "event_callback":
            event = body["event"]
            logging.info(f"Received event_callback: {event['type']}")
            if event["type"] == "user_change":
                UpdateAllProfiles(user_store=self.user_store).execute(body)
                response.ok()
            elif event["type"] == "tokens_revoked":
                UserUninstall(user_store=self.user_store).execute(body)
                response.ok()
            else:
                logging.error("unsupported event_callback")
                response.ok()
        elif type == "shortcut":
            logging.info("shortcut event received")
            response.ok()
        else:
            logging.error("event not supported")
            response.ok()

        return response
