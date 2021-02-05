import hashlib
import hmac
import sys
from time import time
import logging


class VerifyRequest:
    def __init__(self, signing_secret):
        self.signing_secret = signing_secret

    # port of https://github.com/slackapi/python-slack-events-api/blob/d2213d8cad9ba5a930bfd50dacdf9f44c25943d7/slackeventsapi/server.py#L50
    def execute(self, raw_body, headers):
        req_timestamp = headers.get("X-Slack-Request-Timestamp")
        if req_timestamp is None:
            logging.warning("missing X-Slack-Request-Timestamp")
            return False

        timestamp = int(req_timestamp)
        if abs(time() - timestamp) > 60 * 5:
            logging.warning("Invalid request timestamp")
            return False

        signature = headers.get("X-Slack-Signature")
        if signature is None:
            logging.warning("missing timestamp X-Slack-Signature")
            return False

        req = str.encode(f"v0:{timestamp}:{raw_body}")
        request_hash = (
            "v0="
            + hmac.new(str.encode(self.signing_secret), req, hashlib.sha256).hexdigest()
        )

        compare_digest_result = hmac.compare_digest(request_hash, signature)
        logging.warning(f"VerifyRequest {compare_digest_result}")
        return compare_digest_result
