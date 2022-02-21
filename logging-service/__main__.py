from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import simplejson

messages = dict()

class LoggingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(str(list(messages.values())).encode())

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        data = self.rfile.read(content_len)
        data = simplejson.loads(data)
        key = list(data.keys())[0]
        msg = data[key]
        print(msg)
        messages[key] = msg
        
        self.send_response(200)
        self.send_header("Content-length", "0")
        self.end_headers()


def run():
    host_name = "localhost"
    host_port = 9001
    httpd = HTTPServer((host_name, host_port), LoggingHandler)
    print('logging server is running...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
