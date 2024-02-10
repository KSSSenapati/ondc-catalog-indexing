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
            doc['id'] = "doc_" + str(message[message_key])
        elif message_key == "sizesCount":
            updates["sizes_facet"] = "set"
            doc["sizes_facet"] = list(message[message_key])
            for size in list(message[message_key]):
                updates[size + "_size_count"] = "set"
                doc[size + "_size_count"] = message[message_key][size]
        elif message_key == "attributes":
            for attribute in list(message[message_key]):
                updates[attribute + "_atsa"] = "set"
                doc[attribute + "_atsa"] = message[message_key][attribute]
        else:
            updates[message_key] = "set"
            doc[message_key] = message[message_key]
    print(updates, doc)
    return updates, doc

def get_solr_params_to_add(message):
    message = json.loads(message.value.decode('utf-8'))
    doc = {}
    for message_key in message:
        if message_key == "product_id":
            doc[message_key] = message[message_key]
            doc['id'] = "doc_" + str(message[message_key])
        elif message_key == "sizesCount":
            doc["sizes_facet"] = list(message[message_key])
            for size in list(message[message_key]):
                doc[size + "_size_count"] = message[message_key][size]
        elif message_key == "attributes":
            for attribute in list(message[message_key]):
                doc[attribute + "_atsa"] = message[message_key][attribute]
        else:
            doc[message_key] = message[message_key]
    print(doc)
    return doc

def addProduct():
    topic = 'addProduct'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")
        doc = get_solr_params_to_add(message)
        print(doc)
        solr.add([doc])


def deleteProduct():
    topic = 'deleteProduct'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")
        doc_id = "doc_" + str(json.loads(message.value.decode('utf-8'))["product_id"])
        solr.delete(id = doc_id)


def updateProduct(topic):
    topic = 'updateProduct'
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'])
    for message in consumer:
        print(f"Received message in {topic}: {message.value.decode('utf-8')}")
        updates, doc = get_solr_params(message)
        solr.add([doc], fieldUpdates = updates)


if __name__ == "__main__":
    topics = ['addProduct', 'deleteProduct', 'updateProduct', 'updateDiscount', 
              'updateSKU', 'updateRating', 'updateTag', 'updateImage', 'updateAd']

    threads = [threading.Thread(target=updateProduct, args=(topic,)) for topic in topics]
    threads += [threading.Thread(target=addProduct), threading.Thread(target=deleteProduct)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()