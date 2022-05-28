#!/bin/bash

consul kv put hazelcast_nodes "localhost:5701 localhost:5702 localhost:5703"
consul kv put hazelcast_queue "my_queue"
consul kv put hazelcast_map "my_map"