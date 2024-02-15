from streamparse import Bolt
from pymongo import MongoClient
import json

class DeleteBolt(Bolt):
    def initialize(self, stormconf, context):
        solr_url = 'http://localhost:8983/solr/ondc'
        self.solr = pysolr.Solr(solr_url, always_commit=True)

    def process(self, tup):
        message = json.loads(tup.values[0])
        if message['product_id'] is not None:
            try:
                doc_id = f'doc_{message["product_id"]}'
                solr.delete(id=doc_id)
            except Exception as e:
                self.logger.error(f"Error updating document in Solr: {e}")
        else:
            self.logger.error("Missing document ID in message")
