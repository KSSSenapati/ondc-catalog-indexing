from streamparse import Spout
from kafka import KafkaConsumer
import logging
import json

class KafkaSpout(Spout):
    outputs = ['message']

    def initialize(self, stormconf, context):
        self.topic = self.config.get('topic')
        self.consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                      auto_offset_reset='latest',
                                      enable_auto_commit=True,
                                      group_id=None)

        self.consumer.subscribe([self.topic])

    def next_tuple(self):
        for msg in self.consumer:
            self.emit([msg.value.decode('utf-8')])

    def ack(self, tup_id):
        pass

    def fail(self, tup_id):
        pass