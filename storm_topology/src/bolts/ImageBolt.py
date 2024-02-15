from streamparse import Bolt

class ImageBolt(Bolt):
    outputs = ['solr']

    def initialize(self, stormconf, context):
        pass

    def process(self, tup):
        message = json.loads(tup.values[0])
        product_id = message.get('product_id')
        image = message.get('main_image')
        if product_id is not None and image is not None:
            doc = {'id': f'doc_{product_id}', 'main_image': image}
            update = {'main_image': 'set'}
            self.emit({'doc': doc, 'update': update})
