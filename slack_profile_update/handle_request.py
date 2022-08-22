import logging

from slack_profile_update.handle_event import HandleEvent
from slack_profile_update.presenter.api_gateway_request import ApiGatewayRequest
from slack_profile_update.presenter.api_gateway_response import ApiGatewayResponse
from slack_profile_update.usecase.user_install import UserInstall


class HandleRequest:
    def execute(self, *, environment, user_store, event):
        path = event["input"]["path"]
        http_method = event["input"]["requestContext"]["httpMethod"]
        response = ApiGatewayResponse()
        if http_method == "GET":
            if path == "/oauth/authorization_grant":
                query_strings = event["input"]["multiValueQueryStringParameters"]
                code = query_strings.get("code", None)
                state = query_strings.get("state", None)
                if (
                    code is not None
                    and state is not None
                    and len(code) == 1
                    and len(state) == 1
                ):
                    response = UserInstall(
                        client_id=environment["CLIENT_ID"],
                        client_secret=environment["CLIENT_SECRET"],
                        redirect_uri=environment["REDIRECT_URI"],
                        user_store=user_store,
                    ).execute(code[0], state[0])
                else:
                    logging.debug("missing code or state")
                    response.not_found()
            else:
                response.not_found()
        else:
            request = ApiGatewayRequest(event)
            response = HandleEvent(
                environment=environment,
                headers=request.headers(),
                raw_body=request.raw_body(),
                user_store=user_store,
            ).execute()

        return response.present()
