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
```
# in one terminal
ngrok http 8080

# and in another
./tools/localserver.py 8080
````

example user_updated_event

- All users in the workspace create events here...
- new users to the workspace create a event
- updates though the api will need to be checked to stop infinaite feeback loop
- manual clear status creats an event
- automtic status_expiration will create still create an event
	- edge case of status_expiration is propagated for no reason...(may not matter)

we may need to save a hash of the current profile to filter unimportant events

https://api.slack.com/types/user
fileds to check:
	deleted
	is_stranger
fields of intrest
 	updated

