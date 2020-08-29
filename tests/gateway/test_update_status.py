import pytest

from slack_profile_update.gateway.update_status import update_status


@pytest.mark.vcr
def test_can_call_update_status(slack_test_token):
    update_status(
        token=slack_test_token,
        status_text="This is a test!",
        status_emoji=":smile:",
        status_expiration=0
    )
