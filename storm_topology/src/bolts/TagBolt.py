from streamparse import Bolt

class TagBolt(Bolt):
    outputs = ['solr']

    def initialize(self, stormconf, context):
        pass

    def process(self, tup):
        message = json.loads(tup.values[0])
        product_id = message.get('product_id')
        accelerator_tag = message.get('accelerator_tag')
        if product_id is not None and accelerator_tag is not None:
            doc = {'id': f'doc_{product_id}', 'accelerator_tag': accelerator_tag}
            update = {'accelerator_tag': 'set'}
            self.emit({'doc': doc, 'update': update})
