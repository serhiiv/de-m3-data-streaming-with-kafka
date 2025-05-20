import os
import time
import json
import socket
import pandas as pd
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic  # type: ignore


def get_df():
    # prepare data
    # select rows for each producer number

    producer_count = int(os.getenv("PRODUCER_COUNT", 1))
    first_row = 0

    # get the hostname number of the current machine
    # and the first row for this producer
    if producer_count > 1:
        my_ip = socket.gethostbyaddr(socket.gethostname())[2]

        for i in range(producer_count):
            hostname = f"kafka-producer-{i + 1}"
            try:
                if my_ip == socket.gethostbyaddr(hostname)[2]:
                    first_row = i
                    break
            except socket.herror:
                pass

    print("PRODUCER_COUNT:", producer_count)
    print("first_row:", first_row)

    df = pd.read_csv("data/twitter_dataset.csv")
    df = df.iloc[first_row::producer_count]
    print("df.shape:", df.shape)
    print("df:", df.head(producer_count))
    print("--" * 20)
    return df


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(
            f"Delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
        )


def produce(df):
    partition_count = int(os.getenv("PARTITION_COUNT", 1))

    conf = {"bootstrap.servers": "broker:19092"}
    topic_name = "twitter-topic"

    # Create topick with admin function
    admin_client = AdminClient(conf)
    metadata = admin_client.list_topics(timeout=10)

    if topic_name in metadata.topics:
        print(f"Топік '{topic_name}' вже існує.")
    else:
        print(f"Створюємо топік '{topic_name}'...")
        new_topic = NewTopic(
            topic=topic_name, num_partitions=partition_count, replication_factor=1
        )
        fs = admin_client.create_topics([new_topic])
        for topic, f in fs.items():
            try:
                f.result()  # Raise exception if failed
                print(f"Топік '{topic}' створено успішно.")
            except Exception as e:
                print(f"Помилка створення топіка '{topic}': {e}")

    # Producer
    producer = Producer(conf)
    for _, row in df.iterrows():
        producer.poll(0)
        message_key = str(row["Tweet_ID"])
        message_value = row.to_dict()

        producer.produce(
            topic="twitter-topic",
            key=message_key.encode("utf-8"),
            value=json.dumps(message_value).encode("utf-8"),
            callback=delivery_report,
        )
    producer.flush()


if __name__ == "__main__":
    # wait for Kafka to start
    time.sleep(5.0)

    # get dataframe from csv file
    df = get_df()

    produce(df)
