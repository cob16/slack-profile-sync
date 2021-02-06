import json
import logging

from slack_profile_update.usecase.update_all_profiles import UpdateAllProfiles
from slack_profile_update.usecase.url_verification import UrlVerification
from slack_profile_update.usecase.verify_request import VerifyRequest


class HandleEvent:
    def __init__(self, environment, headers, raw_body):
        self.raw_body = raw_body
        self.headers = headers
        self.signing_secret = environment["SLACK_SIGNING_SECRET"]

    def execute(self):
        if not VerifyRequest(signing_secret=self.signing_secret).execute(
            self.raw_body, self.headers
        ):
            return json.dumps({})

        body = json.loads(self.raw_body)

        if body.get("type") == "url_verification":
            return json.dumps(UrlVerification().execute(body))
        elif body["type"] == "event_callback":
            event = body["event"]
            logging.info(f"received event {event['type']}")
            if event["type"] == "user_change":
                UpdateAllProfiles(body).execute()
            else:
                logging.error(f"unsupported event_callback {event}")
        else:
            logging.error("event not supported")
            logging.error(body)

        return ""
