create table "AppUser"
(
    "uid" uuid default gen_random_uuid() not null
        constraint appuser_pkey
            primary key
);

create table "SlackUser"
(
    "slackID" text not null
        constraint slackuser_pk
            primary key,
    "token"   text not null,
    "userID"  uuid
        constraint appuser___fk
            references "AppUser"
);

create index slackuser_userid_index
    on "SlackUser" ("userID");
