import hazelcast
import consul
import argparse
from flask import Flask

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", required=True, type=int)
host_name = "localhost"
host_port = parser.parse_args().port
service_name = "messages-service"

cs = consul.Consul(host=host_name, port=8500)
cs.agent.service.register(service_name,
                          port=host_port,
                          service_id=f"{service_name}:{host_port}")

hz = hazelcast.HazelcastClient(cluster_name="dev",
                               cluster_members=cs.kv.get("hazelcast_nodes")[
                                   1]["Value"].decode("utf-8").split()
                               )
queue = hz.get_queue(cs.kv.get("hazelcast_queue")[
    1]["Value"].decode("utf-8")).blocking()
print("Connected to Hazelcast instance")

app = Flask(__name__)
data = []


@app.get("/")
def do_GET():
    while not queue.is_empty():
        data.append(queue.take())
        print(f"Consumed {data[-1]}")
    return str(data)


if __name__ == "__main__":
    print("message server is running...")
    app.run(host=host_name, port=host_port, debug=True)
