from os import environ

from slack_profile_update.domain.slackuser import SlackUser
from slack_profile_update.gateway.stub_gateway import StubUserGateway


def get_db_name():
    return environ.get("TEST_DATABASE_NAME", "postgres")


def test_create_app_user():
    with StubUserGateway(
        password="pytestPassword", database=get_db_name()
    ).open() as gateway:
        gateway.connection.run("START TRANSACTION")

        assert gateway.test_connection() is True
        user = gateway.create_app_user()

        gateway.connection.run("ROLLBACK")

        assert type(user) is str
        assert user.count("-") == 4


def test_create_slack_user():
    with StubUserGateway(
        password="pytestPassword", database=get_db_name()
    ).open() as gateway:
        gateway.connection.run("START TRANSACTION")

        app_user_id = gateway.create_app_user()
        gateway.create_slack_user(
            SlackUser(user_id="slackid", team_id="teamid", token="test_token"),
            app_user_id=app_user_id,
        )

        gateway.connection.run("ROLLBACK")


def test_get_slack_users():
    with StubUserGateway(
        password="pytestPassword", database=get_db_name()
    ).open() as gateway:
        gateway.connection.run("START TRANSACTION")

        app_user_id = gateway.create_app_user()
        user_1 = SlackUser(user_id="user_1", team_id="team_1", token="test_token_1")
        gateway.create_slack_user(
            user_1,
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
        assert user_1 in results

        gateway.connection.run("ROLLBACK")


def test_get_linked_users():
    with StubUserGateway(
        password="pytestPassword", database=get_db_name()
    ).open() as gateway:
        gateway.connection.run("START TRANSACTION")

        app_user_id = gateway.create_app_user()

        user_1 = SlackUser(user_id="user_1", team_id="team_1", token="test_token_1")
        user_2 = SlackUser(user_id="user_2", team_id="team_2", token="test_token_2")
        user_3 = SlackUser(user_id="user_3", team_id="team_3", token="test_token_3")

        gateway.create_slack_user(user_1, app_user_id)
        gateway.create_slack_user(user_2, app_user_id)
        gateway.create_slack_user(user_3, app_user_id)

        results = gateway.get_linked_users(user_1)
        assert len(results) == 2
        assert user_2 in results
        assert user_3 in results

        gateway.connection.run("ROLLBACK")


def test_connection():
    with StubUserGateway(
        password="pytestPassword", database=get_db_name()
    ).open() as gateway:
        assert gateway.test_connection() is True


def test_get_slack_user():
    with StubUserGateway(
        password="pytestPassword", database=get_db_name()
    ).open() as gateway:
        gateway.connection.run("START TRANSACTION")

        app_user_id = gateway.create_app_user()
        app_user_id_2 = gateway.create_app_user()

        user_1 = SlackUser(user_id="user_1", team_id="team_1", token="test_token_1")
        user_2 = SlackUser(user_id="user_2", team_id="team_2", token="test_token_2")
        user_3 = SlackUser(user_id="user_3", team_id="team_3", token="test_token_3")

        gateway.create_slack_user(user_1, app_user_id)
        gateway.create_slack_user(user_2, app_user_id)
        gateway.create_slack_user(user_3, app_user_id_2)

        user: SlackUser = gateway.get_slack_user(user_id="user_2", team_id="team_2")
        assert user.token == user_2.token

        gateway.connection.run("ROLLBACK")


def test_get_slack_user_when_not_found():
    with StubUserGateway(
        password="pytestPassword", database=get_db_name()
    ).open() as gateway:
        gateway.connection.run("START TRANSACTION")

        app_user_id = gateway.create_app_user()
        user_3 = SlackUser(user_id="user_3", team_id="team_3", token="test_token_3")
        gateway.create_slack_user(user_3, app_user_id)

        user: SlackUser = gateway.get_slack_user(user_id="user_2", team_id="team_2")
        assert user is None

        gateway.connection.run("ROLLBACK")
