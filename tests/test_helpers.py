import hashlib
import hmac
from time import time


def event_signature(secret, timestamp, data):
    req = str.encode("v0:" + str(timestamp) + ":") + str.encode(data)
    request_signature = (
        "v0=" + hmac.new(str.encode(secret), req, hashlib.sha256).hexdigest()
    )
    return request_signature


def event_signature_headers(secret, data):
    timestamp = int(time())
    return {
        "X-Slack-Request-Timestamp": str(int(timestamp)),
        "X-Slack-Signature": event_signature(secret, timestamp, data),
    }
