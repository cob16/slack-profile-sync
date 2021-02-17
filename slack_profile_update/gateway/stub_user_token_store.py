import logging

from slack_profile_update.domain.user import User


class StubUserTokenStore:
    def __init__(self):
        self.user_tokens = {}

    def store(self, user):
        token_key = f"{user.team_id}-|-{user.user_id}"
        logging.debug("stored new token with key %s", token_key)
        self.user_tokens[token_key] = user.token

    def fetch(self, user):
        token = self.user_tokens[f"{user.team_id}-|-{user.user_id}"]
        return User(user_id=user.user_id, team_id=user.team_id, token=token)
