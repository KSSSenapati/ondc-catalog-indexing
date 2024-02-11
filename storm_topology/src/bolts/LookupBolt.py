from streamparse import Bolt
from pymongo import MongoClient

class LookupBolt(Bolt):
    outputs = ['product_id', 'lookup_output']

    def initialize(self, stormconf, context):
        self.mongo_client = MongoClient('localhost', 27017)
        self.db = self.mongo_client['ondc']
        self.collection_name = self.config.get('collection_name')
        self.lookup_attr = self.config.get('lookup_attr')
        self.collection = self.db[self.collection_name]

    def process(self, tup):
        message = json.loads(tup.values[0])
        prod_id = message.get('product_id')
        doc = self.collection.find_one({'product_id': prod_id})
        if doc and self.lookup_attr in doc:
            output = doc[self.lookup_attr]
            self.emit([prod_id, output])
