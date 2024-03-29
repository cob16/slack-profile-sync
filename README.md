# slack-profile-update
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/cob16/slack-profile-sync/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/cob16/slack-profile-sync/tree/main)

## Purpose

To sync current status across workspaces in slack.

For example:
If you set a profile status in one workspace: 

<img src="https://i.imgur.com/b0Gw8ZV.png">

What if that same status was set in your other slack workspaces too! :boom:

## Scope

This is the current scope. In the future, we may look to expand what is synced and to where

# Testing

```bash
make install
```

```bash
make test
```

## Local Run
This codebase is designed to be run inside a lambda but can also be run locally for testing

```# in one terminal
ngrok http 8080
# add the https url returned to your slack app settings page  

# and in another
CLIENT_SECRET="" CLIENT_ID="" SLACK_SIGNING_SECRET="" REDIRECT_URI="" poetry run ./tools/localserver.py 8080
```
