from confluent_kafka import Producer
from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def publish_message(bootstrap_servers, topic, message):
    # Kafka producer configuration
    producer_config = {
        'bootstrap.servers': bootstrap_servers,
        'client.id': 'python-producer'
    }

    # Create Kafka producer
    producer = Producer(producer_config)

    try:
        # Produce message to the specified topic
        producer.produce(topic, value=message, callback=delivery_report)

        # Wait for any outstanding messages to be delivered and delivery reports to be received.
        producer.flush()

    except Exception as e:
        print('Error publishing message: {}'.format(str(e)))

    finally:
        # Close the producer
        producer.close()

if __name__ == "__main__":
    # Kafka bootstrap servers (replace with your actual Kafka broker addresses)
    kafka_bootstrap_servers = os.environ.get("KAFKA_HOST")

    # Kafka topic to publish to
    kafka_topic = os.environ.get("KAFKA_TOPIC")

    # Message to publish
    message_to_publish = 'Hello, Kafka from Python 3!'

    # Publish the message to Kafka
    publish_message(kafka_bootstrap_servers, kafka_topic, message_to_publish)
