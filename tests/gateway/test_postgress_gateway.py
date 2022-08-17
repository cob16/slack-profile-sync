from os import environ

from slack_profile_update.domain.slackuser import SlackUser
from slack_profile_update.gateway.postgress_gateway import PostgressGateway


def get_db_name():
    return environ.get("TEST_DATABASE_NAME", "postgres")


def test_create_app_user():
    with PostgressGateway(
        password="pytestPassword", database=get_db_name()
    ).open() as gateway:
        gateway.connection.run("START TRANSACTION")

        assert gateway.test_connection() is True
        user = gateway.create_app_user()

        gateway.connection.run("ROLLBACK")

        assert type(user) is str
        assert user.count("-") == 4


def test_create_slack_user():
    with PostgressGateway(
        password="pytestPassword", database=get_db_name()
    ).open() as gateway:
        gateway.connection.run("START TRANSACTION")

        app_user_id = gateway.create_app_user()
        gateway.create_slack_user(
            SlackUser(user_id="slackid", team_id="teamid", token="test_token"),
            app_user_id=app_user_id,
        )

        gateway.connection.run("ROLLBACK")


def test_update_slack_user():
    with PostgressGateway(
        password="pytestPassword", database=get_db_name()
    ).open() as gateway:
        gateway.connection.run("START TRANSACTION")

        app_user_id_1 = gateway.create_app_user()
        app_user_id_2 = gateway.create_app_user()
        gateway.create_slack_user(
            SlackUser(user_id="slackid", team_id="teamid", token="test_token_1"),
            app_user_id=app_user_id_1,
        )
        gateway.create_slack_user(
            SlackUser(user_id="slackid", team_id="teamid", token="test_token_2"),
            app_user_id=app_user_id_2,
        )

        assert len(gateway.get_slack_users(app_user_id=app_user_id_1)) == 0

        result = gateway.get_slack_users(app_user_id=app_user_id_2)
        assert len(result) == 1
        assert result[0].token == "test_token_2"

        gateway.connection.run("ROLLBACK")


def test_get_slack_users():
    with PostgressGateway(
        password="pytestPassword", database=get_db_name()
    ).open() as gateway:
        gateway.connection.run("START TRANSACTION")

        app_user_id = gateway.create_app_user()
        gateway.create_slack_user(
            SlackUser(user_id="user_1", team_id="team_1", token="test_token_1"),
            app_user_id=app_user_id,
        )
        gateway.create_slack_user(
            SlackUser(user_id="user_2", team_id="team_2", token="test_token_2"),
            app_user_id=app_user_id,
        )
        gateway.create_slack_user(
            SlackUser(user_id="user_3", team_id="team_3", token="test_token_3"),
            app_user_id=app_user_id,
        )

        results = gateway.get_slack_users(app_user_id=app_user_id)
        assert len(results) == 3
        assert results[0].token == "test_token_1"
        assert results[0].user_id == "user_1"
        assert results[0].team_id == "team_1"

        gateway.connection.run("ROLLBACK")


def test_connection():
    with PostgressGateway(
        password="pytestPassword", database=get_db_name()
    ).open() as gateway:
        assert gateway.test_connection() is True
