import logging

from slack_profile_update.domain.user import User


class UserUninstall:
    def __init__(self, user_link_store, user_token_store):
        self.__user_link_store = user_link_store
        self.__user_token_store = user_token_store

    def execute(self, event_map):
        event = TokenRevokedReader(event_map)
        for user_id in event.user_ids:
            user = User(user_id=user_id, team_id=event.team_id)
            self.__user_link_store.unlink(user)
            user_removed = self.__user_token_store.remove(user)
            if user_removed:
                logging.info("uninstalled user")
            else:
                logging.warning("tried to uninstall user that did not exist")


class TokenRevokedReader:
    def __init__(self, event):
        self.user_ids = event["event"]["tokens"]["oauth"]
        self.team_id = event["team_id"]
