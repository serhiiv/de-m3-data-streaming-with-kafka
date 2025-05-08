# Install Redpanda CLI tools
mkdir -p redpanda
cd redpanda
wget -q https://github.com/redpanda-data/redpanda/releases/latest/download/rpk-linux-amd64.zip


# unzip
unzip rpk-linux-amd64.zip
rm rpk-linux-amd64.zip


# Running a local Redpanda Cluster with Multiple Brokers
wget -q https://docs.redpanda.com/redpanda-labs/docker-compose/_attachments/three-brokers/docker-compose.yml


# Set enviroment
export REDPANDA_VERSION=v25.1.2
export REDPANDA_CONSOLE_VERSION=v3.1.0
export RPK_BROKERS="localhost:19092,localhost:29092,localhost:39092"


# Create containers
docker compose up -d
sleep 3


# Check containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"


# Create a topic
./rpk topic create task1 -r 3 -p 6


# List topics
./rpk topic list


# Describe the topic
./rpk topic describe task1


# Sent at least 10 simple text messages with the console producer
./rpk topic produce task1 -f '%p %k %v\n'


# Receive the messages with the console consumer
./rpk topic consume task1


# Delete the topic
./rpk topic delete task1


# Delete the Kafka cluster
docker compose down -v
cd ..
rm -r redpanda/
