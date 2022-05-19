import hazelcast

hz = hazelcast.HazelcastClient(cluster_name="dev",
                               cluster_members=[
                                   "172.17.0.2:5701",
                                   "172.17.0.3:5701",
                                   "172.17.0.4:5701",
                               ])

map = hz.get_map("my-distributed-map").blocking()
for i in range(1000):
    map.put(i, "value")

hz.shutdown()
