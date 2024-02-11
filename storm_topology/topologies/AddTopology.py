"""
Add topology
"""

from streamparse import Grouping, Topology

from bolts.LookupBolt import LookupBolt
from bolts.AddBolt import AddBolt
from spouts.KafkaSpout import KafkaSpout

class AddTopology(Topology):
    kafka_spout = KafkaSpout.spec(config={'topic': 'addProduct'})
    add_prod_bolt = AddBolt.spec(inputs=[kafka_spout])

    def define_topology(self):
        self.add_spout('kafka_spout', self.kafka_spout)
        self.add_bolt('add_bolt', self.add_prod_bolt)

if __name__ == "__main__":
    AddTopology().run()