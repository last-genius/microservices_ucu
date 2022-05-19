import hazelcast
from time import sleep

hz = hazelcast.HazelcastClient(cluster_name="dev",
                               cluster_members=[
                                   "127.0.0.1:5701",
                                   "127.0.0.1:5702",
                                   "127.0.0.1:5703",
                               ])

queue = hz.get_queue("queue").blocking()

for i in range(1000):
    x = queue.take()
    print(f"Consumed {x}")
    sleep(0.01)
    if x == -1:
        queue.put(x)
        break

print("Consumer finished")

hz.shutdown()
