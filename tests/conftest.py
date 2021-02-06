import os
from pathlib import Path
import pkg_resources
import pytest


@pytest.fixture(scope="session")
def vcr_config():
    return {"filter_headers": ["Authorization"]}


@pytest.fixture(scope="session")
def slack_test_token(pytestconfig):
    if pytestconfig.getoption("record_mode") is "none":
        return "fake_api_token"
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
        path = Path(pkg_resources.resource_filename("tests.resources", filename))
        if path.exists() and path.is_file():
            return path.read_text()
        else:
            raise Exception(f"testfile '{filename}' cannot be found at {path}")

    return _test_file
