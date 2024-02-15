from streamparse import Bolt

class SKUBolt(Bolt):
    outputs = ['solr']

    def initialize(self, stormconf, context):
        pass

    def process(self, tup):
        message = json.loads(tup.values[0])
        product_id = message.get('product_id')
        sizesCount = message.get('sizesCount')
        if product_id is not None and sizesCount is not None:
            doc = {'id': f'doc_{product_id}'}
            update['sizes_facet'] = 'set'
            doc['sizes_facet'] = list(sizesCount)
            for size in list(sizesCount):
                update[f'{size}_size_count'] = 'set'
                doc[f'{size}_size_count'] = sizesCount[size]
            self.emit({'doc': doc, 'update': update})
