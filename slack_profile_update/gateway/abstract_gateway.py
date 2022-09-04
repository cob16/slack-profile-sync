from abc import ABC, abstractmethod
from typing import Optional

from slack_profile_update.domain.slackuser import SlackUser


class AbstractGateway(ABC):
    @abstractmethod
    def create_app_user(self) -> str:
        pass

    @abstractmethod
    def create_slack_user(self, user: SlackUser, app_user_id):
        pass

    @abstractmethod
    def get_slack_user(self, user_id, team_id) -> Optional[SlackUser]:
        pass

    @abstractmethod
    def get_slack_users(self, app_user_id):
        pass

    @abstractmethod
    def get_linked_users(self, user: SlackUser):
        pass

    @abstractmethod
    def delete_slack_user(self, user: SlackUser) -> bool:
        pass
