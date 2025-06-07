import os
import time
import json
import socket
import pandas as pd
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic  # type: ignore


# def get_df():
#     """
#     Read text file with UTF-8 encoding into pandas DataFrame
#     Returns empty DataFrame if file doesn't exist or on error
#     """
#     if not os.path.exists("data/multilingual.txt"):
#         print("File 'data/multilingual.txt' does not exist. Please check the path.")
#         return pd.DataFrame()

#     try:
#         df = pd.read_csv(
#             "data/multilingual.txt",
#             sep=",",              # Use comma as separator
#             encoding="utf-8",     # Specify UTF-8 encoding
#             on_bad_lines="skip"   # Skip lines with wrong number of fields
#         )
#         print("df.shape:", df.shape)
#         print("df:", df.head(2))
#         print("--" * 20)
#         return df

#     except Exception as e:
#         print(f"Error reading file: {e}")
#         return pd.DataFrame()


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(
            f"Delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
        )


def produce():
    conf = {"bootstrap.servers": "broker:19092"}
    topic_name = "raw-tweets-topic"

    # Create topick with admin function
    admin_client = AdminClient(conf)
    metadata = admin_client.list_topics(timeout=10)

    if topic_name in metadata.topics:
        print(f"Topic '{topic_name}' already exists.")
    else:
        print(f"Creating the topic '{topic_name}'...")
        new_topic = NewTopic(topic=topic_name, num_partitions=1, replication_factor=1)
        fs = admin_client.create_topics([new_topic])
        for topic, f in fs.items():
            try:
                f.result()  # Raise exception if failed
                print(f"Topic '{topic}' created successfully.")
            except Exception as e:
                print(f"Error creating topic '{topic}': {e}")

    # Producer
    producer = Producer(conf)

    text = open("data/multilingual.txt").read().split("\n")[:-1]

    for line in text:
        producer.poll(0)
        # Use a timestamp-based key
        message_key = str(int(time.time() * 1000))
        message_value = {"text": line}

        producer.produce(
            topic=topic_name,
            key=message_key.encode("utf-8"),
            value=json.dumps(message_value).encode("utf-8"),
            on_delivery=delivery_report,
        )
        time.sleep(0.001)  # simulate some delay
    producer.flush()


if __name__ == "__main__":
    # # get dataframe from csv file
    # df = get_df()

    # produce messages to kafka topic
    produce()
