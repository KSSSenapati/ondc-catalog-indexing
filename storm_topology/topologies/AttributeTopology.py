"""
Attribute topology
"""

from streamparse import Topology
from spouts.KafkaSpout import KafkaSpout
from bolts.AttributeBolt import AttributeBolt
from bolts.SolrBolt import SolrBolt

class AttributeTopology(Topology):
    kafka_spout = KafkaSpout.spec(config={'topic': 'updateAttribute'})
    attribute_bolt = AttributeBolt.spec(inputs=[kafka_spout])
    solr_bolt = SolrBolt.spec(inputs=[attribute_bolt])

    def define_topology(self):
        self.add_spout('kafka_spout', self.kafka_spout)
        self.add_bolt('attribute_bolt', self.attribute_bolt)
        self.add_bolt('solr_bolt', self.solr_bolt)

if __name__ == "__main__":
    AttributeTopology().run()