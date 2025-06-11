#!/bin/bash

echo
echo "Starting experiment:"
echo
echo "Pull images :"
echo
docker pull apache/kafka:3.9.1
docker pull python:3.12.9-slim
docker build -f prebuilt-images/Dockerfile.faust -t de-module-3-kafka:faust .
docker build -f prebuilt-images/Dockerfile.torch -t de-module-3-kafka:torch .
echo
echo "UP:"
echo
docker compose up -d 
echo
echo "Containers status:"
echo
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo
echo "wait 3 seconds to open Statistics"
sleep 3
echo
x-www-browser "http://localhost:6066/"
sleep 20

echo
while true; do
    read -p "Do you wish to shut down Docker containers? " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo
echo "shutting down Docker containers"
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
echo "delete images"
echo
docker image rm de-module-3-kafka:producer
docker image rm de-module-3-kafka:language
docker image rm de-module-3-kafka:sentiment
docker image rm de-module-3-kafka:person
docker image rm de-module-3-kafka:statistics
docker image rm python:3.12.9-slim
docker image rm apache/kafka:3.9.1
docker image rm de-module-3-kafka:faust
docker image rm de-module-3-kafka:torch
