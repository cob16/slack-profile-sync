import json
import logging

from slack_profile_update.domain.slackuser import SlackUser
from slack_profile_update.gateway.stub_gateway import StubUserGateway
from slack_profile_update.presenter.slack_user_link_model import SlackUserLinkModel
from slack_profile_update.usecase.show_link_user_flow import ShowUserLinkFlow
from slack_profile_update.gateway import slack


def test_show_user_link_flow_calls_slack(test_file, mocker):
    mocker.patch(
        "slack_profile_update.gateway.slack.open_user_dialogue",
        return_value=True,
    )
    payload = json.loads(test_file("parsed_shortcut_event.json"))

    with StubUserGateway().open() as user_store:
        app_user = user_store.create_app_user()
        source_user = SlackUser(
            "U01230123HZ", "32EFEFEFJEFFEI", "token1", app_id=app_user
        )
        user_store.create_slack_user(source_user, app_user)

        ShowUserLinkFlow(user_store=user_store).execute(payload)

        slack.open_user_dialogue.assert_called_once_with(
            trigger_id="34534534535.1329838130354.62ecae7cd230cbb33a7f68a4d0b1fc17",
            token=source_user.token,
            view=SlackUserLinkModel(user_link_id=app_user).present(),
        )


def test_show_user_not_found(caplog, test_file, mocker):
    mocker.patch(
        "slack_profile_update.gateway.slack.open_user_dialogue",
        return_value=True,
    )
    payload = json.loads(test_file("parsed_shortcut_event.json"))

    with StubUserGateway().open() as user_store:
        with caplog.at_level(logging.WARNING):
            ShowUserLinkFlow(user_store=user_store).execute(payload)

            assert not slack.open_user_dialogue.called
            assert f"user model could not be found" in caplog.text, "log does not exist"
