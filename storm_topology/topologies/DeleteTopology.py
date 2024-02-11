"""
Update topology
"""

from streamparse import Grouping, Topology

from bolts.LookupBolt import LookupBolt
from bolts.DeleteBolt import DeleteBolt
from spouts.KafkaSpout import KafkaSpout

class DeleteTopology(Topology):
    kafka_spout = KafkaSpout.spec(config={'topic': 'deleteProduct'})
    delete_bolt = DeleteBolt.spec(inputs=[kafka_spout])

    def define_topology(self):
        self.add_spout('kafka_spout', self.kafka_spout)
        self.add_bolt('delete_bolt', self.delete_bolt)

if __name__ == "__main__":
    DeleteTopology().run()