import requests
import uuid
from flask import Flask, request

app = Flask(__name__)

host_name = "localhost"
host_port = 9000
logging_service = "http://" + host_name + ":9001"
message_service = "http://" + host_name + ":9002"


@app.get("/")
def do_GET():
    log_response = requests.get(logging_service).text
    msg_response = requests.get(message_service).text

    return str(log_response + " | " + msg_response).encode()


@app.post("/")
def do_POST():
    r = requests.post(logging_service, data={"uuid": uuid.uuid4(), "msg": request.get_json()})
    print(r.text)
    return r.text


if __name__ == '__main__':
    print('facade server is running...')
    app.run(host_name, host_port, debug=True)
