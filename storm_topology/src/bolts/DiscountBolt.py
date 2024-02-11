from streamparse import Bolt
from pymongo import MongoClient

class DiscountBolt(Bolt):
    def initialize(self, stormconf, context):
        self.mongo_client = MongoClient('localhost', 27017)
        self.db = self.mongo_client['ondc']
        self.prices_collection = self.db['prices']

    def process(self, tup):
        product_id, price = tup.values[0]
        message = json.loads(tup.values[1])
        discount = message.get('discount')
        if discount:
            discounted_price = price * (1 - (discount / 100))
            self.emit({'product_id': product_id, 'price': discounted_price})
