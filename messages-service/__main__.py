from http.server import BaseHTTPRequestHandler, HTTPServer
import os


class MessageHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("not implemented yet".encode())


def run():
    host_name = "localhost"
    host_port = 9002
    httpd = HTTPServer((host_name, host_port), MessageHandler)
    print('message server is running...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
