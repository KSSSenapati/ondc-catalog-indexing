from streamparse import Bolt

class AdBolt(Bolt):
    def initialize(self, stormconf, context):
        pass

    def process(self, tup):
        message = json.loads(tup.values[0])
        product_id = message.get('product_id')
        ad = message.get('ad')
        if product_id is not None and ad is not None:
            doc = {'id': f'doc_{product_id}', 'ad': ad}
            update = {'ad': 'set'}
            self.emit({'product_id': product_id, 'doc': doc, 'update': update})

