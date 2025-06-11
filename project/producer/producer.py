import time
import json
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic  # type: ignore


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(
            f"Delivered to topic {msg.topic()} key {msg.key()} at offset {msg.offset()}"
        )


def produce():
    conf = {"bootstrap.servers": "broker:19092"}
    topic_name = "tweets-topic"

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
    key_number = 0
    for line in text:
        producer.poll(0)
        message_key = str(key_number).encode("utf-8")
        message_value = {"text": line}
        key_number += 1

        producer.produce(
            topic=topic_name,
            key=message_key,
            value=json.dumps(message_value).encode("utf-8"),
            on_delivery=delivery_report,
        )
        time.sleep(0.01)  # Simulate some delay between messages

    producer.flush()


if __name__ == "__main__":
    produce()
