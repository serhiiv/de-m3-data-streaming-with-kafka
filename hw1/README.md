# Kafka (Redpanda) ecosystem

## Kafka

### Install Kafka CLI tools

[Get Kafka](https://kafka.apache.org/documentation/#quickstart)

```bash
wget https://dlcdn.apache.org/kafka/4.0.0/kafka_2.13-4.0.0.tgz
tar -xzf kafka_2.13-4.0.0.tgz
rm kafka_2.13-4.0.0.tgz
mv kafka_2.13-4.0.0 kafka
cd kafka
```

### Running a local Kafka Cluster with Multiple Brokers

[Kafka Docker Image Usage Guide](https://github.com/apache/kafka/blob/trunk/docker/examples/README.md)

```bash
wget https://raw.githubusercontent.com/apache/kafka/refs/heads/trunk/docker/examples/docker-compose-files/cluster/combined/plaintext/docker-compose.yml

export IMAGE=apache/kafka:4.0.0

docker compose up -d
docker ps
```
### Learn about the kafka cli tools

Create a topic

```bash
bin/kafka-topics.sh --bootstrap-server localhost:29092 --create --topic task1 --partitions 6 --replication-factor 3
```

List topics

```bash
bin/kafka-topics.sh --bootstrap-server localhost:29092 --list
```

Describe the topic

```bash
bin/kafka-topics.sh --bootstrap-server localhost:29092 --describe --topic task1
```

Sent at least 10 simple text messages with the console producer

```bash
bin/kafka-topics.sh --bootstrap-server localhost:29092 --describe --topic task1
```

Receive the messages with the console consumer

```bash
bin/kafka-topics.sh --bootstrap-server localhost:29092 --describe --topic task1
bin/kafka-console-producer.sh --bootstrap-server localhost:29092 --topic task1

bin/kafka-console-consumer.sh --bootstrap-server localhost:29092 --topic task1 --from-beginning
```

Delete the topic

```bash
bin/kafka-topics.sh --bootstrap-server localhost:29092 --delete --topic task1
```

Delete the Kafka cluster

```bash
docker compose down
```


## Redpanda



Running a local Redpanda Cluster with Multiple Brokers
Redpanda CLI tools

1. Set up a Local Kafka Cluster with Multiple Brokers using the Docker Compose tool

```bash
wget https://github.com/apache/kafka/blob/trunk/docker/examples/docker-compose-files/cluster/combined/plaintext/docker-compose.yml

export IMAGE=apache/kafka:latest

```



1. Learn about the kafka cli tools
   1. Create a topic
   2. List topics
   3. Sent at least 10 simple text messages with the console producer
   4. Receive the messages with the console consumer
   5. Delete the topic
2. Learn about the redpanda CLI tool
   1. Create a topic
   2. List topics
   3. Sent at least 10 simple text messages with the console producer
   4. Receive the messages with the console consumer
   5. Delete the topic
