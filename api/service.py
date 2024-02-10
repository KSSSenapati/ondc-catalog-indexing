import json
import pysolr
from kafka import KafkaConsumer
import threading

solr_url = 'http://localhost:8983/solr/ondc'
solr = pysolr.Solr(solr_url, always_commit=True)

def get_solr_params(message):
    message = json.loads(message.value.decode('utf-8'))
    updates = {}
    doc = {}
    for message_key in message:
        if message_key == "product_id":
            doc[message_key] = "doc_" + message[message_key]
        elif message_key == "sizesCount":
            updates["sizes_facet"] = "set"
            doc["sizes_facet"] = list(message[message_key])
            for size in list(message[message_key]):
                updates[size + "_size_count"] = "set"
                doc[size + "_size_count"] = message[message_key][size]
        else:
            updates[message_key] = "set"
            doc[message_key] = message[message_key]
    return updates, doc

def addProduct():
    topic = 'addProduct'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")
        updates, doc = get_solr_params(message)
        solr.add([doc], fieldUpdates = updates)


def deleteProduct():
    topic = 'deleteProduct'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")
        doc_id = "doc_" + json.loads(message.value.decode('utf-8'))["product_id"]
        solr.delete(id = doc_id)


def updateAttributes():
    topic = 'updateAttributes'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")
        updates, doc = get_solr_params(message)
        solr.add([doc], fieldUpdates = updates)


def updateDiscount():
    topic = 'updateDiscount'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")
        updates, doc = get_solr_params(message)
        solr.add([doc], fieldUpdates = updates)


def updateSKU():
    topic = 'updateSKU'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")
        updates, doc = get_solr_params(message)
        solr.add([doc], fieldUpdates = updates)


def updateRating():
    topic = 'updateRating'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")
        updates, doc = get_solr_params(message)
        solr.add([doc], fieldUpdates = updates)


def updateTag():
    topic = 'updateTag'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")
        updates, doc = get_solr_params(message)
        solr.add([doc], fieldUpdates = updates)


def updateImage():
    topic = 'updateImage'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")
        updates, doc = get_solr_params(message)
        solr.add([doc], fieldUpdates = updates)


def updateAd():
    topic = 'updateAd'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")
        updates, doc = get_solr_params(message)
        solr.add([doc], fieldUpdates = updates)


if __name__ == "__main__":
    # Create and start a thread for each consumer function
    threads = [
        threading.Thread(target=addProduct),
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
