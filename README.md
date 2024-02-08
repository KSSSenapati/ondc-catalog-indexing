# ONDC Catalog Indexing - Team Cyborg

### Requirements:
1. docker
2. python3

### Installation:
1. Install python virtual environment:
   ```bash
   python3 -m venv env
   ```
2. Source the virtual environment (run with every new terminal):
   ```bash
   source env/bin/activate
   ```
3. Pull and run docker containers:
   ```bash
   docker-compose up -d
   ```
4. List down running containers
   ```bash
   docker ps
   ```
5. Stop the docker containers
   ```bash
   docker-compose down
   ```
Note: The ```./docker-compose.yml``` file contains zookeeper, kafka, storm-ui, storm-nimbus, storm-supervisor and solr services

### Steps to run Kafka Producer Consumer example:
1. Run the producer script:
   ```bash
   python3 ./kafka/producer.py
   ```
2. Run the consumer script:
   ```bash
   python3 ./kafka/consumer.py
   ```

### Steps to run Flask API example:
1. Run the consumer script:
   ```bash
   python3 ./kafka/consumer.py
   ```
2. Run the flask api script:
   ```bash
   python3 ./kafka/producer_api.py
   ```
3. Call api using curl command
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello from curl!"}' http://localhost:5000/api/push
   ```
