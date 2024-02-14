from streamparse import Bolt

class UpdateBolt(Bolt):
    def initialize(self, stormconf, context):
        pass
    
    def process(self, tup):
        message = json.loads(tup.values[0])
        product_id = message.get('product_id')
        if product_id is not None:
            doc = {'id': f'doc_{product_id}'}
            update = {}
            for key, value in message.items():
                if key == 'product_id':
                    continue
                update[key] = 'set'
                doc[key] = value
            self.emit({'product_id': product_id, 'doc': doc, 'update': update})