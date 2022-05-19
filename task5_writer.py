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
    queue.put(i)
    print(f"Produced {i}")
    sleep(0.01)

queue.put(-1)
print("Producer finished")

hz.shutdown()
