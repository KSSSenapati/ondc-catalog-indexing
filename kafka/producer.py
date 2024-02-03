from kafka import KafkaProducer
import time

# Kafka configuration
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'test'

# Create Kafka producer
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

# Produce messages
for i in range(10):
    message = f"Message {i}"
    producer.send(kafka_topic, value=message.encode('utf-8'))
    print(f"Produced: {message}")
    time.sleep(1)  # Simulate some processing time

# Flush and close producer
producer.flush()
producer.close()

