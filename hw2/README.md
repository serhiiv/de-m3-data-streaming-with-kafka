# Kafka (Redpanda) ecosystem

Репозиторій і посилання на статті, які допомогли розібратися з запуском broker, consumer and produser Kafka в одному контейнері
 [Kafka Listeners - Explained](https://github.com/rmoff/kafka-listeners/tree/master)
 

### Running a local Kafka Cluster


```bash

export IMAGE=apache/kafka:4.0.0

docker compose up -d
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```





Delete the Kafka cluster

```bash
docker compose down -v
```

