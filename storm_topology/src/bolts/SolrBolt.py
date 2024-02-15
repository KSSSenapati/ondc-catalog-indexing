from streamparse import Bolt
import json
import pysolr

class SolrBolt(Bolt):
    outputs = ['default']

    def initialize(self, stormconf, context):
        solr_url = 'http://localhost:8983/solr/ondc'
        self.solr = pysolr.Solr(solr_url, always_commit=True)
        
    def process(self, tup):
        doc, update = tup.values[0]
        if doc is not None and update is not None:
            try:
                doc_id = doc.get('id')
                self.solr.add([doc], fieldUpdates=update)
                self.logger.info(f"Document with ID {doc_id} updated in Solr")
            except Exception as e:
                self.logger.error(f"Error updating document in Solr: {e}")
