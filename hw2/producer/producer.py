import json
import pandas as pd
from confluent_kafka import Producer


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(
            f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
        )


def main():
    conf = {"bootstrap.servers": "broker:19092"}

    producer = Producer(conf)

    df = pd.read_csv("data/twitter_dataset_test.csv")
    for _, row in df.iterrows():
        message_key = str(row["Tweet_ID"])
        message_value = row.to_dict()

        producer.produce(
            topic="twitter-topic-0",
            key=message_key.encode("utf-8"),
            value=json.dumps(message_value).encode("utf-8"),
            callback=delivery_report,
        )
        producer.poll(0)

    producer.flush()


if __name__ == "__main__":
    main()
