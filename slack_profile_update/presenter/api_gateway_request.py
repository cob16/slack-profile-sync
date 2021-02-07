class ApiGatewayRequest:
    def __init__(self, event):
        self.__event = event

    def raw_body(self):
        return self.__event["input"]["body"]

    def headers(self):
        return self.__event["input"]["headers"]
