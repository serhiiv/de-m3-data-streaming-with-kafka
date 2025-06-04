#!/bin/bash

echo
echo "Starting experiment:"
echo
# echo "Build :"
# echo
# docker compose build --no-cache --pull --progress plain
# echo
echo "UP:"
echo
docker compose up -d 
echo
echo "Containers status:"
echo
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo
echo "wait 5 seconds to open top domains"
sleep 5
echo
x-www-browser "http://localhost:6066/top"
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
docker image rm producer:latest
docker image rm streams:latest
docker image rm apache/kafka:3.9.1
