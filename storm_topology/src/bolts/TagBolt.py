from streamparse import Bolt

class TagBolt(Bolt):
    def initialize(self, stormconf, context):
        pass

    def process(self, tup):
        product_id, tag = tup.values[0]
        if product_id is not None and tag is not None:
            doc = {'id': f'doc_{product_id}', 'accelerator_tag': tag}
            update = {'accelerator_tag': 'set'}
            self.emit({'product_id': product_id, 'doc': doc, 'update': update})
