import json
import logging

from slack_profile_update.presenter.api_gateway_response import ApiGatewayResponse
from slack_profile_update.usecase.update_all_profiles import UpdateAllProfiles
from slack_profile_update.usecase.url_verification import UrlVerification
from slack_profile_update.usecase.verify_request import VerifyRequest


class HandleEvent:
    def __init__(self, environment, headers, raw_body):
        self.raw_body = raw_body
        self.headers = headers
        self.signing_secret = environment["SLACK_SIGNING_SECRET"]

    def execute(self):
        response = ApiGatewayResponse()
        if not VerifyRequest(signing_secret=self.signing_secret).execute(
            self.raw_body, self.headers
        ):
            response.auth_error()
            return response

        body = json.loads(self.raw_body)

        type = body.get("type")
        if type == "url_verification":
            response_body = UrlVerification().execute(body)
            response.ok(response_body)
        elif type == "event_callback":
            event = body["event"]
            logging.info(f"received event {event['type']}")
            if event["type"] == "user_change":
                UpdateAllProfiles(body).execute()
                response.ok()
            else:
                logging.error("unsupported event_callback %s", event)
                response.ok()
        else:
            logging.error("event not supported %s", body)
            response.ok()

        return response
