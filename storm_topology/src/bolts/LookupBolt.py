from streamparse import Bolt
from pymongo import MongoClient

class LookupBolt(Bolt):
    outputs = ['prod_id', 'price']

    def initialize(self, stormconf, context):
        self.mongo_client = MongoClient('localhost', 27017)
        self.db = self.mongo_client['ondc']
        self.prices_collection = self.db['prices']

    def process(self, tup):
        prod_id = tup.values[0]
        price_document = self.prices_collection.find_one({'prod_id': prod_id})
        if price_document:
            price = price_document['price']
            self.emit([prod_id, price])
