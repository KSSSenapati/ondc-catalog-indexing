from streamparse import Spout
from kafka import KafkaConsumer
import logging

class KafkaSpout(Spout):
    outputs = ['prod_id', 'discount']

    def initialize(self, stormconf, context):
        self.consumer = KafkaConsumer('discount', bootstrap_servers='localhost:9092',
                                      group_id='my-group', auto_offset_reset='latest')
        logging.basicConfig(level=logging.ERROR,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def next_tuple(self):
        for message in self.consumer:
            prod_id, discount = message.value.split(',')
            my_tuple = [prod_id.strip(), float(discount.strip())]
            logging.error("Emitted tuple: %s", my_tuple)
            self.emit(my_tuple)

