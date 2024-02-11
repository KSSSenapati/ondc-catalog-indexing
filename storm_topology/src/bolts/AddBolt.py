from streamparse import Bolt
from pymongo import MongoClient
import json

class AddBolt(Bolt):
    def initialize(self, stormconf, context):
        solr_url = 'http://localhost:8983/solr/ondc'
        self.solr = pysolr.Solr(solr_url, always_commit=True)

    def get_solr_param(message):
        doc = dict()
        for key, value in message.items():
            if key == 'product_id':
                doc['id'] = f'doc_{value}'
            elif key == 'sizesCount':
                doc['sizes_facet'] = list(value)
                for size in list(value):
                    doc[f'{size}_size_count'] = value[size]
            elif key == 'attribute':
                for attr in list(value):
                    doc[f'{attr}_atsa'] = value[attr]
            else:
                doc[key] = value
        return doc

    def process(self, tup):
        message = json.loads(tup.values[0])
        doc_id = message.get('product_id')
        if doc_id:
            try:
                updates, doc = self.get_solr_param(message)
                self.solr.add([doc])
                self.logger.info(f"Document with ID {doc_id} added in Solr")
            except Exception as e:
                self.logger.error(f"Error updating document in Solr: {e}")
        else:
            self.logger.error("Missing document ID in message")


if __name__ == "__main__":
    AddBolt().run()