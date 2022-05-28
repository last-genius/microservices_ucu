import requests
import uuid
import hazelcast
import consul
from flask import Flask, request
from random import choice

app = Flask(__name__)
host_name = "localhost"
host_port = 9000
service_name = "facade-service"

cs = consul.Consul(host=host_name, port=8500)
cs.agent.service.register(service_name,
                               port=host_port,
                               service_id=f"{service_name}:{host_port}")

logging_service = []
message_service = []
for key, val in cs.agent.services().items():
    print(key, val)
    if key.startswith("logging-service"):
        logging_service.append(f"http://localhost:{val['Port']}")
    elif key.startswith("messages-service"):
        message_service.append(
            f"http://localhost:{val['Port']}")
print(logging_service)
print(message_service)

hz = hazelcast.HazelcastClient(cluster_name="dev",
                               cluster_members=cs.kv.get("hazelcast_nodes")[1]["Value"].decode("utf-8").split()
                               )

queue = hz.get_queue(cs.kv.get(
    "hazelcast_queue")[1]["Value"].decode("utf-8")).blocking()
print("Connected to Hazelcast instance")


@app.get("/")
def do_GET():
    log_response = requests.get(choice(logging_service)).text
    msg_response = requests.get(choice(message_service)).text

    return str(log_response + " | " + msg_response).encode()


@app.post("/")
def do_POST():
    queue.put(f"{request.get_json()}")
    r = requests.post(choice(logging_service), data={
                      "uuid": uuid.uuid4(), "msg": request.get_json()})
    print(r.text)
    return r.text


if __name__ == "__main__":
    print("facade server is running...")
    app.run(host_name, host_port, debug=True)
