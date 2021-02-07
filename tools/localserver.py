#!/usr/bin/env python3

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import logging

from slack_profile_update.handle_request import HandleRequest


class S(BaseHTTPRequestHandler):
    def do_GET(self):
        print(parse.urlparse(self.path).path)
        if parse.urlparse(self.path).path != "/oauth/authorization_grant":
            self.send_error(404)
        else:
            print(self.path)

            response = HandleRequest().execute(
                os.environ,
                event=self.api_gateway_proxy_event(None, "GET"),
            )
            logging.debug(f"returning {response}")

            self.handle_response(response)

    def do_POST(self):
        content_length = int(
            self.headers["Content-Length"]
        )  # <--- Gets the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")

        logging.info(
            "POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
            str(self.path),
            str(self.headers),
            post_data,
        )

        event = self.api_gateway_proxy_event(post_data, "POST")

        response = HandleRequest().execute(os.environ, event)
        self.handle_response(response)

    def api_gateway_proxy_event(self, post_data, http_method):
        querys = parse.urlparse(self.path).query
        query_arguments = {}
        if querys != "":
            query_arguments = parse.parse_qs(querys, strict_parsing=True)
        return {
            "input": {
                "path": parse.urlparse(self.path).path,
                "requestContext": {
                    "httpMethod": http_method,
                },
                "headers": self.headers,
                "multiValueQueryStringParameters": query_arguments,
                "body": post_data,
            },
        }

    def handle_response(self, response):
        logging.debug(f"returning {response}")

        self.send_response(response["statusCode"])
        self.send_headers(response["headers"])
        self.end_headers()
        if response["body"] is not None:
            self.wfile.write(response["body"].encode())

    def send_headers(self, header_dict):
        for key, value in header_dict.items():
            self.send_header(key, value)


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.DEBUG)

    server_address = ("", port)
    httpd = server_class(server_address, handler_class)

    logging.info("Starting httpd...\n")

    try:

        httpd.serve_forever()

    except KeyboardInterrupt:

        pass

    httpd.server_close()

    logging.info("Stopping httpd...\n")


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
