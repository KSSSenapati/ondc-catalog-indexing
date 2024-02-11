"""
Discount topology
"""

from streamparse import Grouping, Topology

from bolts.LookupBolt import LookupBolt
from bolts.UpdateBolt import UpdateBolt
from spouts.KafkaSpout import KafkaSpout

class DiscountTopology(Topology):
    kafka_spout = KafkaSpout.spec()
    lookup_bolt = LookupBolt.spec(inputs={kafka_spout: Grouping.fields(['prod_id'])})
    update_bolt = UpdateBolt.spec(inputs={lookup_bolt: Grouping.fields(['prod_id']),
                                                     kafka_spout: Grouping.fields(['prod_id'])})
