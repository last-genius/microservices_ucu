## Task 1

Installed Hazelcast

## Task 2

![](./img/task2.jpg)

## Task 3

With all nodes present, data is spread roughly equally: 

![](./img/task3-1.png)

With only two nodes present:

![](./img/task3-2.png)

With only one node present:

![](./img/task3-3.png)

As we can see, there is no loss of data and it's spread equally between the present nodes.

## Task 4

![](./img/task4.png)

## Task 5 

Here is a blocked writer that has filled the queue, with no readers yet:

![](./img/task5-1.png)
![](./img/task5-2.png)

After launching two readers, they've unloaded the queue completely, taking different elements:

![](./img/task5-3.png)
![](./img/task5-4.png)
![](./img/task5-5.png)
