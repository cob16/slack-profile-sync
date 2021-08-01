import logging

from slack_profile_update.domain.slackuser import SlackUser


class StubUserTokenStore:
    def __init__(self):
        self.user_tokens = {}

    def store(self, user):
        logging.debug(
            f"stored team: '{user.team_id}' user: '{user.user_id}' new token with key '{user.token}'"
        )
        self.user_tokens[self.__user_key(user)] = user.token

    def fetch(self, user):
        token = self.user_tokens[f"{user.team_id}-|-{user.user_id}"]
        return SlackUser(user_id=user.user_id, team_id=user.team_id, token=token)

    def remove(self, user):
        try:
            del self.user_tokens[self.__user_key(user)]
            return True
        except KeyError:
            return False

    def __user_key(self, user: SlackUser) -> str:
        return f"{user.team_id}-|-{user.user_id}"
