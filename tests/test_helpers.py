from time import time

from slack_sdk.signature import SignatureVerifier


def event_signature_headers(secret, data):
    timestamp = str(int(time()))
    return {
        "X-Slack-Request-Timestamp": str(int(timestamp)),
        "X-Slack-Signature": SignatureVerifier(secret).generate_signature(
            timestamp=timestamp, body=data
        ),
    }
