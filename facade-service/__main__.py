import requests
import uuid
import hazelcast
from flask import Flask, request
from random import choice

app = Flask(__name__)

hz = hazelcast.HazelcastClient(cluster_name="dev",
                               cluster_members=[
                                   "127.0.0.1:5701",
                                   "127.0.0.1:5702",
                                   "127.0.0.1:5703"
                               ])
print("Connected to Hazelcast instance")
queue = hz.get_queue("my-queue").blocking()

host_name = "localhost"
host_port = 9000
logging_service = ["http://" + host_name + f":{i}" for i in [9002, 9003, 9004]]
message_service =  ["http://" + host_name + f":{i}" for i in [9005, 9006]]


@app.get("/")
def do_GET():
    log_response = requests.get(choice(logging_service)).text
    msg_response = requests.get(choice(message_service)).text

    return str(log_response + " | " + msg_response).encode()


@app.post("/")
def do_POST():
    queue.put(f"{request.get_json()}")
    r = requests.post(choice(logging_service), data={"uuid": uuid.uuid4(), "msg": request.get_json()})
    print(r.text)
    return r.text


if __name__ == '__main__':
    print('facade server is running...')
    app.run(host_name, host_port, debug=True)
