import requests
import uuid
from flask import Flask, request
from random import choice

app = Flask(__name__)

host_name = "localhost"
host_port = 9000
message_service = "http://" + host_name + ":9001"
logging_service = ["http://" + host_name + f":{i}" for i in [9002, 9003, 9004]]


@app.get("/")
def do_GET():
    log_response = requests.get(choice(logging_service)).text
    msg_response = requests.get(message_service).text

    return str(log_response + " | " + msg_response).encode()


@app.post("/")
def do_POST():
    r = requests.post(choice(logging_service), data={"uuid": uuid.uuid4(), "msg": request.get_json()})
    print(r.text)
    return r.text


if __name__ == '__main__':
    print('facade server is running...')
    app.run(host_name, host_port, debug=True)
