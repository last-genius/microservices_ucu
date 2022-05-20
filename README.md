## Task 3

After launching one facade service, one messaging service and three logging services (connected to three Hazelcast nodes),
we can send messages through the facade service.

![](./img/1.png)

A GET request after all POST requests:
![](./img/2.png)

Since logging services are chosen randomly from a list by the facade service, each one
of them receives only several messages:

![](./img/3.png)
![](./img/4.png)
![](./img/5.png)

Since we are chosing logging services from a pre-defined list, we encounter errors
after suspending some of them, but we are still able to read messages from the remaining
Hazelcast nodes
