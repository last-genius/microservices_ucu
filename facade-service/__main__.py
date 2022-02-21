from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import requests
import uuid

host_name = "localhost"
host_port = 9000
logging_service = "http://" + host_name + ":9001"
message_service = "http://" + host_name + ":9002"


class FacadeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        r = requests.get(logging_service)
        log_response = r.text

        r = requests.get(message_service)
        msg_response = r.text

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(str(log_response + " | " + msg_response).encode())

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        r = requests.post(logging_service, json={str(uuid.uuid4()): self.rfile.read(content_len)})

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


def run():
    httpd = HTTPServer((host_name, host_port), FacadeHandler)
    print('facade server is running...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
