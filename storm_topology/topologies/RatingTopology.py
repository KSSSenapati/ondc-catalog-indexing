"""
Rating topology
"""

from streamparse import Topology
from spouts.KafkaSpout import KafkaSpout
from bolts.RatingBolt import RatingBolt
from bolts.SolrBolt import SolrBolt

class RatingTopology(Topology):
    kafka_spout = KafkaSpout.spec(config={'topic': 'updateRating'})
    rating_bolt = RatingBolt.spec(inputs=[kafka_spout])
    solr_bolt = SolrBolt.spec(inputs=[rating_bolt])

    def define_topology(self):
        self.add_spout('kafka_spout', self.kafka_spout)
        self.add_bolt('rating_bolt', self.rating_bolt)
        self.add_bolt('solr_bolt', self.solr_bolt)

if __name__ == "__main__":
    RatingTopology().run()