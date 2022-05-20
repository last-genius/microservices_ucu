import hazelcast
from flask import Flask, request

hz = hazelcast.HazelcastClient(cluster_name="dev",
                               cluster_members=[
                                   "127.0.0.1:5701",
                                   "127.0.0.1:5702",
                                   "127.0.0.1:5703"
                               ])
print("Connected to Hazelcast instance")
queue = hz.get_queue("my-queue").blocking()

app = Flask(__name__)
data = []


@app.get("/")
def do_GET():
    while not queue.is_empty():
        data.append(queue.take())
        print(f"Consumed {data[-1]}")
    return str(data)


if __name__ == '__main__':
    print('message server is running...')
    app.run()
