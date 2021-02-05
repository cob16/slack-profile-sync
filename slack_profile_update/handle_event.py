import json

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
        return json.dumps(UrlVerification().execute(body))
