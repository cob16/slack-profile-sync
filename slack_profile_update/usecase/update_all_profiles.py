import logging


class UpdateAllProfiles:
    def __init__(self, update_event):
        self.update_event = update_event

    def execute(self):
        event = UpdateEventReader(self.update_event)
        logging.debug(
            "update event of user: '%s' USERID: '%s' TEAMID: '%s'"
            " to status text: '%s' emoji '%s' expiration: '%s'",
            event.name,
            event.user_id,
            event.team_id,
            event.status_text,
            event.status_emoji,
            event.status_expiration,
        )


class UpdateEventReader:
    def __init__(self, event):
        self.name = event["event"]["user"]["name"]
        self.user_id = event["event"]["user"]["id"]
        self.team_id = event["event"]["user"]["team_id"]
        self.status_text = event["event"]["user"]["profile"]["status_text"]
        self.status_emoji = event["event"]["user"]["profile"]["status_emoji"]
        self.status_expiration = event["event"]["user"]["profile"]["status_expiration"]
