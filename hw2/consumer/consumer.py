import sys
import time
# import json
from datetime import datetime
from confluent_kafka import Consumer


def main():
    conf = {
        "bootstrap.servers": "broker:19092",
        "group.id": "twitter-consumer-group",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(conf)
    consumer.subscribe(["twitter-topic-0"])

    print("Listening for tweets...")
    try:
        # while True:
        for _ in range(20):
            # Poll for new messages
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            tweet_id = msg.key().decode("utf-8")
            # tweet_data = json.loads(msg.value().decode("utf-8"))
            print(
                f"tweet_id: {tweet_id}, tweet_size: {sys.getsizeof(msg.value())}, produser_timestamp: {datetime.fromtimestamp(msg.timestamp()[1] / 1000)}"
            )

            time.sleep(0.01)  # опціональна затримка

    except KeyboardInterrupt:
        print("\nStopping consumer...")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
