from streamparse import Bolt

class RatingBolt(Bolt):
    def initialize(self, stormconf, context):
        pass

    def process(self, tup):
        message = json.loads(tup.values[0])
        product_id = message.get('product_id')
        rating = message.get('rating')
        if product_id is not None and rating is not None:
            doc = {'id': f'doc_{product_id}', 'rating': rating}
            update = {'rating': 'set'}
            self.emit({'product_id': product_id, 'doc': doc, 'update': update})

