from streamparse import Bolt

class AttributeBolt(Bolt):
    outputs = ['solr']

    def initialize(self, stormconf, context):
        pass

    def process(self, tup):
        message = json.loads(tup.values[0])
        product_id = message.get('product_id')
        attribute = message.get('attribute')
        if product_id is not None and attribute is not None:
            doc = {'id': f'doc_{product_id}'}
            update = {}
            for attr in list(attribute):
                doc[f'{attr}_atsa'] = attribute[attr]
                update[f'{attr}_atsa'] = 'set'
            self.emit({'doc': doc, 'update': update})
