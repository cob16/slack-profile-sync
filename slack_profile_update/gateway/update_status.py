from slack import WebClient


def update_status(
    token: str, status_text: str, status_emoji: str, status_expiration: int
):
    client = WebClient(token=token)

    payload = dict(
        profile=dict(
            status_text=status_text,
            status_emoji=status_emoji,
            status_expiration=status_expiration,
        )
    )
    client.users_profile_set(**payload)
