from contextlib import contextmanager
from typing import Optional

import pg8000.native

from slack_profile_update.domain.slackuser import SlackUser
from slack_profile_update.gateway.abstract_gateway import AbstractGateway


class PostgressGateway:
    def __init__(self, password, database, user="postgres"):
        self.user = user
        self.password = password
        self.database = database

    @contextmanager
    def open(self):
        con = None
        try:
            con = pg8000.native.Connection(
                self.user, password=self.password, database=self.database
            )
            gateway = self._InnerGateway(connection=con)
            yield gateway
        finally:
            if con:
                con.close()

    class _InnerGateway(AbstractGateway):
        def __init__(self, connection):
            self.connection = connection

        def test_connection(self):
            self.connection.run("SELECT 1")
            return True

        def create_app_user(self):
            result = self.connection.run(
                'INSERT INTO "AppUser"(uid) VALUES(DEFAULT) RETURNING "uid";'
            )
            return str(result[0][0])

        def create_slack_user(self, user, app_user_id):
            slack_id = self._user_to_slack_id(user)
            self.connection.run(
                'INSERT INTO "SlackUser"("slackID", "userID", "token") VALUES(:slackID, :userID, :token) ON CONFLICT ("slackID") DO UPDATE SET "userID" = excluded."userID", "token" = EXCLUDED."token" ;',
                slackID=slack_id,
                userID=app_user_id,
                token=user.token,
            )

        def _user_to_slack_id(self, user):
            return self._to_slack_id(user_id=user.user_id, team_id=user.team_id)

        def _to_slack_id(self, user_id, team_id):
            return f"{team_id}-|-{user_id}"

        def get_slack_users(self, app_user_id):
            results = self.connection.run(
                'SELECT "slackID", "token" FROM "SlackUser" WHERE "userID" = :userID',
                userID=app_user_id,
            )
            return self._as_slack_user(results)

        def delete_slack_user(self, user: SlackUser) -> bool:
            result = self.connection.run(
                'DELETE FROM "SlackUser" WHERE "slackID" = :slackID RETURNING *',
                slackID=self._user_to_slack_id(user),
            )
            return bool(result)

        def get_slack_user(self, user_id, team_id) -> Optional[SlackUser]:
            slack_id = self._to_slack_id(user_id=user_id, team_id=team_id)
            result = self.connection.run(
                'SELECT "slackID", "token", "userID" FROM "SlackUser" WHERE "slackID" = :slackID',
                slackID=slack_id,
            )
            if result:
                user = result[0]
                ids = user[0].split("-|-")
                return SlackUser(
                    team_id=ids[0], user_id=ids[1], token=user[1], app_id=str(user[2])
                )
            return None

        def get_linked_users(self, user: SlackUser):
            slack_id = self._user_to_slack_id(user)
            user = self.connection.run(
                'SELECT "userID" FROM "SlackUser" WHERE "slackID" = :slackID',
                slackID=slack_id,
            )
            if user:
                results = self.connection.run(
                    'SELECT "slackID", "token" FROM "SlackUser" WHERE "userID" = :userID AND  "slackID" != :slackID',
                    userID=user[0][0],
                    slackID=slack_id,
                )
                return self._as_slack_user(results)
            else:
                return []

        def _as_slack_user(self, results):
            users = []
            for r in results:
                ids = r[0].split("-|-")
                users.append(SlackUser(team_id=ids[0], user_id=ids[1], token=r[1]))
            return users
