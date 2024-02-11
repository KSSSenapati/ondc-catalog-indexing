from streamparse import Bolt
import json
import pysolr

class UpdateBolt(Bolt):
    def initialize(self, stormconf, context):
        solr_url = 'http://localhost:8983/solr/ondc'
        self.solr = pysolr.Solr(solr_url, always_commit=True)

    def get_solr_param(message):
        doc, updates = dict(), dict()
        for key, value in message.items():
            if key == 'product_id':
                doc['id'] = f'doc_{value}'
            elif key == 'sizesCount':
                updates[key] = 'set'
                doc['sizes_facet'] = list(value)
                for size in list(value):
                    updates[f'{size}_size_count'] = 'set'
                    doc[f'{size}_size_count'] = value[size]
            elif key == 'attribute':
                for attr in list(value):
                    updates[f'{attr}_atsa'] = 'set'
                    doc[f'{attr}_atsa'] = value[attr]
            else:
                updates[key] = 'set'
                doc[key] = value
        return updates, doc

    def process(self, tup):
        message = json.loads(tup.values[0])
        doc_id = message.get('product_id')
        if doc_id:
            try:
                updates, doc = self.get_solr_param(message)
                self.solr.add([doc], fieldUpdates=updates)
                self.logger.info(f"Document with ID {doc_id} updated in Solr")
            except Exception as e:
                self.logger.error(f"Error updating document in Solr: {e}")
        else:
            self.logger.error("Missing document ID in message")


if __name__ == "__main__":
    UpdateBolt().run()