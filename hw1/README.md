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
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
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
bin/kafka-console-producer.sh --bootstrap-server localhost:29092 --topic task1
```

Receive the messages with the console consumer

```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:29092 --topic task1 --from-beginning
```

Delete the topic

```bash
bin/kafka-topics.sh --bootstrap-server localhost:29092 --delete --topic task1
```

Delete the Kafka cluster

```bash
docker compose down
cd ..
rm -r kafka/
```


## Redpanda

### Install Redpanda CLI tools

[Get Redpanda](https://docs.redpanda.com/current/get-started/rpk-install/)

```bash
mkdir -p redpanda
cd redpanda
wget https://github.com/redpanda-data/redpanda/releases/latest/download/rpk-linux-amd64.zip
unzip rpk-linux-amd64.zip
rm rpk-linux-amd64.zip
```

### Running a local Redpanda Cluster with Multiple Brokers

```bash
wget https://docs.redpanda.com/redpanda-labs/docker-compose/_attachments/three-brokers/docker-compose.yml
```



1. Set up a Local Kafka Cluster with Multiple Brokers using the Docker Compose tool

```bash
wget https://docs.redpanda.com/redpanda-labs/docker-compose/_attachments/three-brokers/docker-compose.yml

export REDPANDA_VERSION=v25.1.2
export REDPANDA_CONSOLE_VERSION=v3.1.0
docker compose up -d

docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Open Redpanda Console at [localhost:8080](http://localhost:8080/)

### Learn about the Redpanda CLI tool

```bash
export RPK_BROKERS="localhost:19092,localhost:29092,localhost:39092"
```

Create a topic

```bash
./rpk topic create task1 -r 3 -p 6
```

List topics

```bash
./rpk topic list
```

Describe the topic

```bash
./rpk topic describe task1
```

Sent at least 10 simple text messages with the console producer

```bash
./rpk topic produce task1 -f '%p %k %v\n'

0 key0 value0	
1 key1 value1
```

Receive the messages with the console consumer

```bash
export RPK_BROKERS="localhost:19092,localhost:29092,localhost:39092"
./rpk topic consume task1
```

Delete the topic

```bash
./rpk topic delete task1
```

Delete the Kafka cluster

```bash
docker compose down -v
cd ..
rm -r redpanda/
```

