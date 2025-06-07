#!/bin/bash

echo
echo "Starting experiment:"
echo
# echo "Build :"
# echo
# docker compose build --no-cache --push --progress plain
# echo
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
docker image rm apache/kafka:3.9.1
docker image rm local-producer:latest
docker image rm local-language:latest
docker image rm local-sentiment:latest
docker image rm local-person:latest
docker image rm local-statistics:latest
