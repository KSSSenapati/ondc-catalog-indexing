"""
Discount topology
"""

from streamparse import Topology
from spouts.KafkaSpout import KafkaSpout
from bolts.LookupBolt import LookupBolt
from bolts.DiscountBolt import DiscountBolt
from bolts.SolrBolt import SolrBolt

class DiscountTopology(Topology):
    kafka_spout = KafkaSpout.spec(config={'topic': 'updateDiscount'})
    lookup_bolt = LookupBolt.spec(config={'lookup_attr': 'price'}, inputs=[kafka_spout])
    discount_bolt = DiscountBolt.spec(inputs=[lookup_bolt])
    solr_bolt = SolrBolt.spec(inputs=[discount_bolt])

    def define_topology(self):
        self.add_spout('kafka_spout', self.kafka_spout)
        self.add_bolt('lookup_bolt', self.lookup_bolt)
        self.add_bolt('discount_bolt', self.discount_bolt)
        self.add_bolt('solr_bolt', self.solr_bolt)

if __name__ == "__main__":
    DiscountTopology().run()