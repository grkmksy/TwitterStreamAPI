# Twitter Stream API with Apache Kafka Integration

This python code is streaming Twitter data to your local Apache Kafka topic as json objects, based on your specified stream filters. 

# Requirements
  - [Python3.0](https://www.python.org/) or above must be installed.
  - [tweepy](https://github.com/tweepy/tweepy) python library must be installed.
  - [kafka-python](https://github.com/dpkp/kafka-python) library must be installed
  - Apache Kafka must be installed.

### Apache Kafka Installation

Download and Install latest release of Apache Kafka. (Ubuntu 16.04 & CentOS 7)
```sh
$ wget http://ftp.itu.edu.tr/Mirror/Apache/kafka/1.0.0/kafka_2.11-1.0.0.tgz
```
Step 1 : Extract Files
```sh
$ tar -xzf kafka_2.11-1.0.0.tgz
$ cd kafka_2.11-1.0.0
```

Step 2 : Start ZooKeeper & Kafka Servers
```sh
$ bin/zookeeper-server-start.sh config/zookeeper.properties
$ bin/kafka-server-start.sh config/server.properties
```

Step 3 : Create a Kafka Topic
```sh
$ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic kafka-social
```

Step 4: List active Kafka Topics 
```sh
$ bin/kafka-topics.sh --list --zookeeper localhost:2181
```

Step 5 : Test Kafka Producer & Send Some Messages
```sh
$ bin/kafka-console-producer.sh --broker-list localhost:9092 --topic kafka-social
```


Step 6 : Test Kafka Consumer & Dump Some Messages
```sh
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic kafka-social --from-beginning
```
After successful completion of these operations, you can start stream api and write tweets to your kafka topic.
