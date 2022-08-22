from collections import defaultdict
from contextlib import contextmanager

from slack_profile_update.domain.slackuser import SlackUser
from unittest.mock import MagicMock
import uuid

from slack_profile_update.gateway.abstract_gateway import AbstractGateway


class StubUserGateway:
    def __init__(self, **kwargs):
        pass

    @contextmanager
    def open(self):
        yield self._InnerGateway()

    class _InnerGateway(AbstractGateway):
        def __init__(self):
            self.connection = MagicMock()
            self._users = defaultdict(lambda: set())

        def test_connection(self):
            return True

        def create_app_user(self) -> str:
            return str(uuid.uuid4())

        def create_slack_user(self, user: SlackUser, app_user_id):
            self._users[app_user_id].add(user)

        def get_slack_users(self, app_user_id):
            return list(self._users[app_user_id])

        def get_linked_users(self, user: SlackUser):
            for stored_user_set in self._users.values():
                if user in stored_user_set:
                    return list(stored_user_set.difference({user}))
            return []

        def delete_slack_user(self, user: SlackUser):
            print(f"removing {self._users.values()}")
            for stored_user_set in self._users.values():
                print(f"{stored_user_set}")
                try:
                    stored_user_set.remove(user)
                    return True
                except KeyError:
                    continue

            return False
