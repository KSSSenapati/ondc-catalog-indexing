"""
Discount topology
"""

from streamparse import Topology
from spouts.KafkaSpout import KafkaSpout
from bolts.LookupBolt import LookupBolt
from bolts.DiscountBolt import DiscountBolt
from bolts.UpdateBolt import UpdateBolt

class DiscountTopology(Topology):
    kafka_spout = KafkaSpout.spec(config={'topic': 'updateDiscount'})
    lookup_bolt = LookupBolt.spec(inputs=[kafka_spout])
    discount_bolt = DiscountBolt.spec(inputs=[lookup_bolt, kafka_spout])
    update_bolt = UpdateBolt.spec(inputs=[discount_bolt])

    def define_topology(self):
        self.add_spout('kafka_spout', self.kafka_spout)
        self.add_bolt('lookup_bolt', self.lookup_bolt)
        self.add_bolt('discount_bolt', self.discount_bolt)
        self.add_bolt('update_bolt', self.update_bolt)

if __name__ == "__main__":
    DiscountTopology().run()