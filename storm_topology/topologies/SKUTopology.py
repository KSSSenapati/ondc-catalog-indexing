"""
SKU topology
"""

from streamparse import Topology
from spouts.KafkaSpout import KafkaSpout
from bolts.LookupBolt import LookupBolt
from bolts.SKUBolt import SKUBolt
from bolts.SolrBolt import SolrBolt

class SKUTopology(Topology):
    kafka_spout = KafkaSpout.spec(config={'topic': 'updateSKU'})
    lookup_bolt = LookupBolt.spec(config={'lookup_attr': 'sizesCount'}, inputs=[kafka_spout])
    sku_bolt = SKUBolt.spec(inputs=[lookup_bolt])
    solr_bolt = SolrBolt.spec(inputs=[sku_bolt])

    def define_topology(self):
        self.add_spout('kafka_spout', self.kafka_spout)
        self.add_bolt('lookup_bolt', self.lookup_bolt)
        self.add_bolt('sku_bolt', self.sku_bolt)
        self.add_bolt('solr_bolt', self.solr_bolt)

if __name__ == "__main__":
    SKUTopology().run()