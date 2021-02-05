# slack-profile-update

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
poetry install  
```

```bash
make test
```

## Local Run (to receive events)

```# in one terminal
ngrok http 8080

# and in another
./tools/localserver.py 8080
```
