"""
Update topology
"""

from streamparse import Grouping, Topology

from bolts.LookupBolt import LookupBolt
from bolts.UpdateBolt import UpdateBolt
from spouts.KafkaSpout import KafkaSpout

class UpdateTopology(Topology):
    kafka_spout = KafkaSpout.spec(config={'topic': 'updateProduct'})
    update_bolt = UpdateBolt.spec(inputs=[kafka_spout])

    def define_topology(self):
        self.add_spout('kafka_spout', self.kafka_spout)
        self.add_bolt('update_bolt', self.update_bolt)

if __name__ == "__main__":
    UpdateTopology().run()