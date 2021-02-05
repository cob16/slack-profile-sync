import json

from slack_profile_update.usecase.url_verification import UrlVerification


def handle_event(event):
    HandleEvent(event).execute()


class HandleEvent:

    def __init__(self, event):
        self.event = json.loads(event)

    def execute(self):
        return json.dumps(UrlVerification().execute(self.event))

