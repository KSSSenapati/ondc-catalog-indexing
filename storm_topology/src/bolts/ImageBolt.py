from streamparse import Bolt

class ImageBolt(Bolt):
    def initialize(self, stormconf, context):
        pass

    def process(self, tup):
        product_id, image = tup.values[0]
        if product_id is not None and image is not None:
            doc = {'id': f'doc_{product_id}', 'main_image': image}
            update = {'main_image': 'set'}
            self.emit({'product_id': product_id, 'doc': doc, 'update': update})
