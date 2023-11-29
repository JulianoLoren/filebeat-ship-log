from confluent_kafka import Consumer, KafkaError
from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

def consume_messages(bootstrap_servers, group_id, topics):
    # Kafka consumer configuration
    consumer_config = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }

    # Create Kafka consumer
    consumer = Consumer(consumer_config)

    # Subscribe to the specified topics
    consumer.subscribe(topics)

    try:
        while True:
            # Poll for messages
            msg = consumer.poll(1.0)  # 1-second timeout

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event, not an error
                    continue
                else:
                    print('Error: {}'.format(msg.error()))
                    break

            # Process the received message
            print('Received message: {}'.format(msg.value().decode('utf-8')))

    except KeyboardInterrupt:
        pass

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

if __name__ == "__main__":
    # Kafka bootstrap servers (replace with your actual Kafka broker addresses)
    kafka_bootstrap_servers = os.environ.get("KAFKA_HOST")

    # Kafka consumer group ID
    kafka_group_id = os.environ.get("KAFKA_GROUP_ID")

    # Kafka topics to subscribe to
    kafka_topics = [os.environ.get("KAFKA_TOPIC")]

    # Consume messages from Kafka
    consume_messages(kafka_bootstrap_servers, kafka_group_id, kafka_topics)
