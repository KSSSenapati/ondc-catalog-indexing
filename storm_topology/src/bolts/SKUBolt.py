from streamparse import Bolt

class SKUBolt(Bolt):
    def initialize(self, stormconf, context):
        pass

    def process(self, tup):
        product_id, sku = tup.values[0]
        if product_id is not None and sku is not None:
            doc = {'id': f'doc_{product_id}'}
            update['sizes_facet'] = 'set'
            doc['sizes_facet'] = list(sku)
            for size in list(sku):
                update[f'{size}_size_count'] = 'set'
                doc[f'{size}_size_count'] = sku[size]
            self.emit({'product_id': product_id, 'doc': doc, 'update': update})
