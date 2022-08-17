from contextlib import contextmanager

import pg8000.native

from slack_profile_update.domain.slackuser import SlackUser


class PostgressGateway:
    def __init__(self, password, database, user="postgres"):
        self.user = user
        self.password = password
        self.database = database

    @contextmanager
    def open(self):
        try:
            con = pg8000.native.Connection(
                self.user, password=self.password, database=self.database
            )
            gateway = self._InnerGateway(connection=con)
            yield gateway
        finally:
            con.close()

    class _InnerGateway:
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
            slack_id = f"{user.team_id}-|-{user.user_id}"
            self.connection.run(
                'INSERT INTO "SlackUser"("slackID", "userID", "token") VALUES(:slackID, :userID, :token) ON CONFLICT ("slackID") DO UPDATE SET "userID" = excluded."userID", "token" = EXCLUDED."token" ;',
                slackID=slack_id,
                userID=app_user_id,
                token=user.token,
            )

        def get_slack_users(self, app_user_id):
            results = self.connection.run(
                'SELECT "slackID", "token" FROM "SlackUser" WHERE "userID" = :userID',
                userID=app_user_id,
            )
            users = []
            for r in results:
                ids = r[0].split("-|-")
                users.append(SlackUser(team_id=ids[0], user_id=ids[1], token=r[1]))
            return users
