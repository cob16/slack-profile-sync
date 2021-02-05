import json

from slack_profile_update.handle_event import HandleEvent


def test_handle_url_verification_event(test_file):
    event = test_file('example_url_verification_event.json')

    responce = HandleEvent(event).execute()

    assert responce == '{"challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P"}'

