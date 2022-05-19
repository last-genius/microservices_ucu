import timeit

set_up = '''
import hazelcast
from time import sleep
hz = hazelcast.HazelcastClient(cluster_name="dev",
                               cluster_members=[
                                   "172.17.0.2:5701",
                                   "172.17.0.3:5701",
                                   "172.17.0.4:5701",
                               ])

map = hz.get_map("my-distributed-map").blocking()
'''

no_locking = '''
key = "1"
map.put(key, 0)

for i in range(1000):
    val = map.get(key)
    sleep(0.01)
    val += 1
    map.put(key, val)

print(f"Finished! Result = {map.get(key)}")
'''

pess_locking = '''
key = "1"
map.put(key, 0)

for i in range(1000):
    map.lock(key)
    try:
        val = map.get(key)
        sleep(0.01)
        val += 1
        map.put(key, val)
    finally:
        map.unlock(key)

print(f"Finished! Result = {map.get(key)}")
'''

opt_locking = '''
key = "1"
map.put(key, 0)

for i in range(1000):
    while True:
        new_val = old_val = map.get(key)
        sleep(0.01)
        new_val += 1
        if map.replace_if_same(key, old_val, new_val):
            break


print(f"Finished! Result = {map.get(key)}")
'''


print("No locks execution time:",
      timeit.timeit(setup=set_up,
                    stmt=no_locking,
                    number=1))

print("Pessimistic locks execution time:",
      timeit.timeit(setup=set_up,
                    stmt=pess_locking,
                    number=1))

print("Optimistic locks execution time:",
      timeit.timeit(setup=set_up,
                    stmt=opt_locking,
                    number=1))

# hz.shutdown()
