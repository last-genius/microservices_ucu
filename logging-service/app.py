import hazelcast
from flask import Flask, request

app = Flask(__name__)

host_name = "localhost"

hz = hazelcast.HazelcastClient(cluster_name="dev",
                                       cluster_members=[
                                           "127.0.0.1:5701",
                                           "127.0.0.1:5702",
                                           "127.0.0.1:5703"
                                       ])
print("Connected to Hazelcast instance")

messages = hz.get_map("my-map").blocking()


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


if __name__ == '__main__':
    print('logging server is running...')
    app.run()
