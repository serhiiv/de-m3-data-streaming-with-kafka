# Install Kafka CLI tools
wget -q https://dlcdn.apache.org/kafka/4.0.0/kafka_2.13-4.0.0.tgz


# untar
tar -xzf kafka_2.13-4.0.0.tgz

# go to workdir
rm kafka_2.13-4.0.0.tgz
mv kafka_2.13-4.0.0 kafka
cd kafka


# Running a local Kafka Cluster with Multiple Brokers
wget -q https://raw.githubusercontent.com/apache/kafka/refs/heads/trunk/docker/examples/docker-compose-files/cluster/combined/plaintext/docker-compose.yml


# select image
export IMAGE=apache/kafka:4.0.0


# create containers
docker compose up -d
sleep 3


# check containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"


# Create a topic
bin/kafka-topics.sh --bootstrap-server localhost:29092 --create --topic task1 --partitions 6 --replication-factor 3


# List topics
bin/kafka-topics.sh --bootstrap-server localhost:29092 --list


# Describe the topic
bin/kafka-topics.sh --bootstrap-server localhost:29092 --describe --topic task1


# Sent at simple text messages with the console producer
bin/kafka-console-producer.sh --bootstrap-server localhost:29092 --topic task1


# Receive the messages with the console consumer
bin/kafka-console-consumer.sh --bootstrap-server localhost:29092 --topic task1 --from-beginning


# Delete the topic
bin/kafka-topics.sh --bootstrap-server localhost:29092 --delete --topic task1


# Delete the Kafka cluster
docker compose down
cd ..
rm -r kafka/
