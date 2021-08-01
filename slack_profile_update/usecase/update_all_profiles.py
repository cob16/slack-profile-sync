import logging

from slack_profile_update.domain.slackuser import SlackUser
from slack_profile_update.gateway import slack


class UpdateAllProfiles:
    def __init__(self, user_link_store, user_token_store):
        self.user_link_store = user_link_store
        self.user_token_store = user_token_store

    def execute(self, update_event):
        event = UpdateEventReader(update_event)
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
        try:
            user_list = self.user_link_store.fetch(
                SlackUser(event.user_id, event.team_id)
            )
            for user in user_list:
                user_with_token = self.user_token_store.fetch(user)
                slack.update_status(
                    token=user_with_token.token,
                    status_text=event.status_text,
                    status_emoji=event.status_emoji,
                    status_expiration=event.status_expiration,
                )
        except KeyError:
            pass


class UpdateEventReader:
    def __init__(self, event):
        self.name = event["event"]["user"]["name"]
        self.user_id = event["event"]["user"]["id"]
        self.team_id = event["event"]["user"]["team_id"]
        self.status_text = event["event"]["user"]["profile"]["status_text"]
        self.status_emoji = event["event"]["user"]["profile"]["status_emoji"]
        self.status_expiration = event["event"]["user"]["profile"]["status_expiration"]
