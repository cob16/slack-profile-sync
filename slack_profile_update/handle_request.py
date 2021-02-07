from slack_profile_update.handle_event import HandleEvent
from slack_profile_update.presenter.api_gateway_request import ApiGatewayRequest
from slack_profile_update.presenter.api_gateway_response import ApiGatewayResponse
from slack_profile_update.usecase.authorization_grant import AuthorizationGrant


class HandleRequest:
    def execute(self, environment, event):
        path = event["input"]["path"]
        http_method = event["input"]["requestContext"]["httpMethod"]
        response = ApiGatewayResponse()
        if http_method == "GET":
            if path == "/oauth/authorization_grant":
                code = event["input"]["queryStringParameters"].get("code", None)
                state = event["input"]["queryStringParameters"].get("state", None)
                if code is not None and state is not None:
                    body = AuthorizationGrant().execute(code, state)
                    response.ok_html(body)
                else:
                    response.not_found()
            else:
                response.not_found()
        else:
            request = ApiGatewayRequest(event)
            response = HandleEvent(
                environment=environment,
                headers=request.headers(),
                raw_body=request.raw_body(),
            ).execute()

        return response.present()
