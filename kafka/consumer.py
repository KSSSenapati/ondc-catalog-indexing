from kafka import KafkaConsumer

# Kafka configuration
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'test'

# Create Kafka consumer
consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=kafka_bootstrap_servers,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group'
)

# Consume messages
for message in consumer:
    print(f"Received: {message.value.decode('utf-8')}")

# Close consumer (not necessary for this example as it runs indefinitely)
# consumer.close()

