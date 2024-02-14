"""
Update topology
"""

from streamparse import Topology
from bolts.UpdateBolt import UpdateBolt
from bolts.SolrBolt import SolrBolt
from spouts.KafkaSpout import KafkaSpout

class UpdateTopology(Topology):
    kafka_spout = KafkaSpout.spec(config={'topic': 'updateProduct'})
    update_bolt = UpdateBolt.spec(inputs=[kafka_spout])
    solr_bolt = SolrBolt.spec(inputs=[update_bolt])

    def define_topology(self):
        self.add_spout('kafka_spout', self.kafka_spout)
        self.add_bolt('update_bolt', self.update_bolt)
        self.solr_bolt('solr_bolt', self.solr_bolt)

if __name__ == "__main__":
    UpdateTopology().run()