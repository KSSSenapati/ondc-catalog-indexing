from streamparse import Bolt
from pymongo import MongoClient

class UpdateBolt(Bolt):
    def initialize(self, stormconf, context):
        self.mongo_client = MongoClient('localhost', 27017)
        self.db = self.mongo_client['ondc']
        self.prices_collection = self.db['prices']

    def process(self, tup):
        prod_id, price = tup.values
        discount = tup.values[1]  # Discount received from KafkaSpout
        discounted_price = price * (1 - (discount / 100))
        # Update the discounted price in MongoDB
        self.prices_collection.update_one({'prod_id': prod_id}, {'$set': {'price': discounted_price}}, upsert=True)
        self.emit([prod_id, discounted_price])