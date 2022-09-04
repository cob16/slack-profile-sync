class SlackUserLinkModel:
    def __init__(self, user_link_id):
        self.user_link_id = user_link_id

    def present(self):
        return {
            "type": "modal",
            "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
            "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
            "title": {"type": "plain_text", "text": "Link user status", "emoji": True},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "Enter the AppUserId of another user account to link status or copy this ID to preform this action in another account:",
                        "emoji": True,
                    },
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"`{self.user_link_id}`"},
                },
                {"type": "divider"},
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "user-link-code",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "AppUserId",
                        "emoji": False,
                    },
                },
            ],
        }
