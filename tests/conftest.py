import hashlib
import hmac
import os
from pathlib import Path
from time import time

import pkg_resources
import pytest


@pytest.fixture(scope="session")
def vcr_config():
    return {"filter_headers": ["Authorization"]}


@pytest.fixture(scope="session")
def slack_test_token(pytestconfig):
    if pytestconfig.getoption("record_mode") is "none":
        return "foobar"
    else:
        token = os.environ.get("SLACK_API_TOKEN", None)
        if token is None:
            raise ValueError(
                "please provide slack api key using 'SLACK_API_TOKEN' env "
                "var when using the slack api for real"
            )
        return token


@pytest.fixture()
def test_file():
    def _test_file(filename):
        print(pkg_resources.resource_filename("tests.resources", filename))
        path = Path(pkg_resources.resource_filename("tests.resources", filename))
        if path.exists() and path.is_file():
            return path.read_text()
        else:
            raise Exception(f"testfile '{filename}' cannot be found")

    return _test_file


def __create_signature(secret, timestamp, data):
    req = str.encode("v0:" + str(timestamp) + ":") + str.encode(data)
    request_signature = (
        "v0=" + hmac.new(str.encode(secret), req, hashlib.sha256).hexdigest()
    )
    return request_signature


@pytest.fixture()
def create_signature():
    return __create_signature


@pytest.fixture()
def create_signature_headers():
    def create_signature_headers(secret, data):
        timestamp = int(time())
        return {
            "X-Slack-Request-Timestamp": str(int(timestamp)),
            "X-Slack-Signature": __create_signature(secret, timestamp, data),
        }

    return create_signature_headers
