import sys
import time
from datetime import datetime
from confluent_kafka import Consumer
from prometheus_client import start_http_server, Gauge


def main():
    throughput_mbps = Gauge(
        "consumer_throughput_megabytes_total", "Throughput of the system in Mbps"
    )
    latency_sec = Gauge(
        "consumer_latency_seconds", "Latency_of message processing"
    )

    conf = {
        "bootstrap.servers": "broker:19092",
        "group.id": "twitter-consumer-group",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(conf)
    consumer.subscribe(["twitter-topic"])

    print("Listening for tweets...")
    try:
        while True:
            # Poll for new messages
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            tweet_id = msg.key().decode("utf-8")
            m_bps = sys.getsizeof(msg.value()) / 1024 / 1024
            latency = (
                datetime.now() - datetime.fromtimestamp(msg.timestamp()[1] / 1000)
            ).total_seconds()
            print(f"tweet_id: {tweet_id}, Mbps: {m_bps}, latency: {latency}")

            # Imitates processing by sleeping for 1 sec,
            time.sleep(1.0)

            # Record the size of the tweet in MB and the latency
            throughput_mbps.inc(m_bps)
            latency_sec.set(latency)

    except KeyboardInterrupt:
        print("\nStopping consumer...")
    finally:
        consumer.close()


if __name__ == "__main__":
    # wait for Kafka to start
    time.sleep(10.0)

    start_http_server(8000)

    main()
