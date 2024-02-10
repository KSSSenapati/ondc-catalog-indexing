import json
import pysolr
from kafka import KafkaConsumer
import threading

solr_url = 'http://localhost:8983/solr/your_collection_name'
solr = pysolr.Solr(solr_url, always_commit=True)


def addProduct():
    topic = 'addProduct'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")


def queryProduct():
    topic = 'queryProduct'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")


def deleteProduct():
    topic = 'deleteProduct'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")


def updateAttributes():
    topic = 'updateAttributes'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")


def updateDiscount():
    topic = 'updateDiscount'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")


def updateSKU():
    topic = 'updateSKU'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")


def updateRating():
    topic = 'updateRating'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")


def updateTag():
    topic = 'updateTag'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")


def updateImage():
    topic = 'updateImage'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")


def updateAd():
    topic = 'updateAd'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")


if __name__ == "__main__":
    # Create and start a thread for each consumer function
    threads = [
        threading.Thread(target=addProduct),
        threading.Thread(target=queryProduct),
        threading.Thread(target=deleteProduct),
        threading.Thread(target=updateAttributes),
        threading.Thread(target=updateDiscount),
        threading.Thread(target=updateSKU),
        threading.Thread(target=updateRating),
        threading.Thread(target=updateTag),
        threading.Thread(target=updateImage),
        threading.Thread(target=updateAd)
    ]
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
