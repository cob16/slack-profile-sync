import logging

from slack_profile_update.domain.slackuser import SlackUser


class UserUninstall:
    def __init__(self, user_store):
        self.__user_store = user_store

    def execute(self, event_map):
        event = TokenRevokedReader(event_map)
        for user_id in event.user_ids:
            user = SlackUser(user_id=user_id, team_id=event.team_id)
            user_removed = self.__user_store.delete_slack_user(user)
            if user_removed:
                logging.info("uninstalled user")
            else:
                logging.warning("tried to uninstall user that did not exist")


class TokenRevokedReader:
    def __init__(self, event):
        self.user_ids = event["event"]["tokens"]["oauth"]
        self.team_id = event["team_id"]
