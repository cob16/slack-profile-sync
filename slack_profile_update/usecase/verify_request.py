import logging

from slack_sdk.signature import SignatureVerifier


class VerifyRequest:
    def __init__(self, signing_secret):
        self.signing_secret = signing_secret

    def execute(self, raw_body, headers):
        is_valid = SignatureVerifier(self.signing_secret).is_valid_request(
            headers=headers, body=raw_body
        )
        if not is_valid:
            logging.warning(f"SignatureVerifier returned {is_valid}")
        return is_valid
