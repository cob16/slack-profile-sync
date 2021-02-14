import logging


class StubUserTokenStore:
    def __init__(self):
        self.user_tokens = {}

    def store(self, team_id, user_id, token):
        token_key = f"{team_id}-|-{user_id}"
        logging.debug("stored new token with key %s", token_key)
        self.user_tokens[token_key] = token

    def fetch(self, team_id, user_id):
        return self.user_tokens[f"{team_id}-|-{user_id}"]
