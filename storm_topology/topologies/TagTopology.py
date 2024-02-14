"""
Tag topology
"""

from streamparse import Topology
from spouts.KafkaSpout import KafkaSpout
from bolts.LookupBolt import LookupBolt
from bolts.TagBolt import TagBolt
from bolts.SolrBolt import SolrBolt

class TagTopology(Topology):
    kafka_spout = KafkaSpout.spec(config={'topic': 'updateTag'})
    lookup_bolt = LookupBolt.spec(config={'lookup_attr': 'accelerator_tag'}, inputs=[kafka_spout])
    tag_bolt = TagBolt.spec(inputs=[lookup_bolt])
    solr_bolt = SolrBolt.spec(inputs=[tag_bolt])

    def define_topology(self):
        self.add_spout('kafka_spout', self.kafka_spout)
        self.add_bolt('lookup_bolt', self.lookup_bolt)
        self.add_bolt('tag_bolt', self.tag_bolt)
        self.add_bolt('solr_bolt', self.solr_bolt)

if __name__ == "__main__":
    TagTopology().run()