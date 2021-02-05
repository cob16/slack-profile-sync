import json


class UrlVerification:
    def execute(self, event):
        return {"challenge": event["challenge"]}
