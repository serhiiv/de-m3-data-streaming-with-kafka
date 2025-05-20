#!/bin/bash
echo
echo "Select experiment configuration:"
echo
echo "  1) 1 producer,  1 partition,   1 consumer"
echo "  2) 1 producer,  1 partition,   2 consumers"
echo "  3) 1 producer,  2 partitions,  2 consumers"
echo "  4) 1 producer,  5 partitions,  5 consumers"
echo "  5) 1 producer,  10 partitions, 1 consumers"
echo "  6) 1 producer,  10 partitions, 5 consumers"
echo "  7) 1 producer,  10 partitions, 10 consumers"
echo "  8) 2 producers, 10 partitions, 10 consumers"
echo
read -p "Please enter your choice: " n
echo
case $n in
    1) export PRODUCER_COUNT=1; export PARTITION_COUNT=1; export CONSUMER_COUNT=1;;
    2) export PRODUCER_COUNT=1; export PARTITION_COUNT=1; export CONSUMER_COUNT=2;;
    3) export PRODUCER_COUNT=1; export PARTITION_COUNT=2; export CONSUMER_COUNT=2;;
    4) export PRODUCER_COUNT=1; export PARTITION_COUNT=5; export CONSUMER_COUNT=5;;
    5) export PRODUCER_COUNT=1; export PARTITION_COUNT=10; export CONSUMER_COUNT=1;;
    6) export PRODUCER_COUNT=1; export PARTITION_COUNT=10; export CONSUMER_COUNT=5;;
    7) export PRODUCER_COUNT=1; export PARTITION_COUNT=10; export CONSUMER_COUNT=10;;
    8) export PRODUCER_COUNT=2; export PARTITION_COUNT=10; export CONSUMER_COUNT=10;;
    *) echo "invalid option"; exit;;
esac

echo
echo "Starting experiment"
docker compose up -d 
sleep wait 10 seconds
sleep 10

echo
echo "containers status"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
sleep wait 15 seconds
sleep 15

# uncomment to see prometheus web interface
# echo
# echo "opening prometheus"
# x-www-browser http://localhost:9090
# sleep 1

echo
echo "opening grafana admin/admin"
x-www-browser "http://localhost:3000/d/ea51098d-97b3-4d18-b72e-748a296f402b/kafka-based-experiment?orgId=1&from=now-5m&to=now&timezone=Europe%2FKyiv&refresh=5s"
sleep 10

echo
while true; do
    read -p "Do you wish to shut down Docker? " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo
echo "shutting down Docker"
docker compose down

echo
while true; do
    read -p "Do you wish to delete images? " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo
echo "delete images:"
docker image rm producer:latest
docker image rm consumer:latest
docker image rm prom/prometheus:latest
docker image rm grafana/grafana:latest
docker image rm apache/kafka:latest
