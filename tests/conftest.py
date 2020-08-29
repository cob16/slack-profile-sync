import pytest


@pytest.fixture(scope="session")
def vcr_config():
    return {"filter_headers": ["Authorization"]}

@pytest.fixture(scope="session")
def slack_test_token(pytestconfig):
    if pytestconfig.getoption('record_mode') is 'none':
        return "foobar"
    else:
        raise ValueError(f"you must provide a valid api key if using the slack api for real")

