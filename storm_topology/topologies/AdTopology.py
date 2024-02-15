"""
Ad topology
"""

from streamparse import Topology
from spouts.KafkaSpout import KafkaSpout
from bolts.AdBolt import AdBolt
from bolts.SolrBolt import SolrBolt

class AdTopology(Topology):
    kafka_spout = KafkaSpout.spec(config={'topic': 'updateAd'})
    ad_bolt = AdBolt.spec(inputs=[kafka_spout])
    solr_bolt = SolrBolt.spec(inputs=[ad_bolt])

    def define_topology(self):
        self.add_spout('kafka_spout', self.kafka_spout)
        self.add_bolt('ad_bolt', self.ad_bolt)
        self.add_bolt('solr_bolt', self.solr_bolt)

if __name__ == "__main__":
    AdTopology().run()