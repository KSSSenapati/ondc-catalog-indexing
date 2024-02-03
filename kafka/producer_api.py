from flask import Flask, request, jsonify
from kafka import KafkaProducer

# Kafka configuration
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'test'

# Create Kafka producer
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

# Initialize Flask app
app = Flask(__name__)

# API endpoint to push data to Kafka
@app.route('/api/push', methods=['POST'])
def push_to_kafka():
    data = request.json

    if data is None or 'message' not in data:
        return jsonify({'error': 'Invalid request. Message is required.'}), 400

    message = data['message']

    # Push message to Kafka
    try:
        producer.send(kafka_topic, value=message.encode('utf-8'))
        producer.flush()
        return jsonify({'status': 'success', 'message': 'Data pushed to Kafka successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

