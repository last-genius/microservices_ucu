import hazelcast
import consul
import argparse
from flask import Flask, request

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", required = True, type=int)
host_name = "localhost"
host_port = parser.parse_args().port
service_name = "logging-service"

cs = consul.Consul(host=host_name, port=8500)
cs.agent.service.register(service_name,
                               port=host_port,
                               service_id=f"{service_name}:{host_port}")

hz = hazelcast.HazelcastClient(cluster_name="dev",
                               cluster_members=cs.kv.get("hazelcast_nodes")[1]["Value"].decode("utf-8").split()
                               )
messages = hz.get_map(cs.kv.get("hazelcast_map")[
                      1]["Value"].decode("utf-8")).blocking()
print("Connected to Hazelcast instance")


@app.get("/")
def do_GET():
    return str(list(messages.values()))


@app.post("/")
def do_POST():
    key = str(request.form["uuid"])
    msg = request.form["msg"]
    print(msg)

    messages.lock(key)
    try:
        messages.put(key, msg)
    finally:
        messages.unlock(key)

    return ""


if __name__ == "__main__":
    print("logging server is running...")
    app.run(host=host_name, port=host_port, debug=True)
