"""
Image topology
"""

from streamparse import Topology
from spouts.KafkaSpout import KafkaSpout
from bolts.LookupBolt import LookupBolt
from bolts.ImageBolt import ImageBolt
from bolts.SolrBolt import SolrBolt

class ImageTopology(Topology):
    kafka_spout = KafkaSpout.spec(config={'topic': 'updateImage'})
    lookup_bolt = LookupBolt.spec(config={'lookup_attr': 'main_image'}, inputs=[kafka_spout])
    image_bolt = ImageBolt.spec(inputs=[lookup_bolt])
    solr_bolt = SolrBolt.spec(inputs=[image_bolt])

    def define_topology(self):
        self.add_spout('kafka_spout', self.kafka_spout)
        self.add_bolt('lookup_bolt', self.lookup_bolt)
        self.add_bolt('image_bolt', self.image_bolt)
        self.add_bolt('solr_bolt', self.solr_bolt)

if __name__ == "__main__":
    ImageTopology().run()
