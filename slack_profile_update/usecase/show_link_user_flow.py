import logging

import slack_profile_update.gateway.slack as slack
from slack_profile_update.domain.slackuser import SlackUser
from slack_profile_update.presenter.slack_user_link_model import SlackUserLinkModel


class ShowUserLinkFlow:
    def __init__(self, user_store):
        self.user_store = user_store

    def execute(self, payload):
        user: SlackUser = self.user_store.get_slack_user(
            user_id=payload["user"]["id"], team_id=payload["user"]["team_id"]
        )
        if user:
            view = SlackUserLinkModel(user_link_id=user.app_id).present()
            slack.open_user_dialogue(
                token=user.token, trigger_id=payload["trigger_id"], view=view
            )
        else:
            logging.warning("user model could not be found")
