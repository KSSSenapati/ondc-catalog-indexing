from streamparse import Bolt

class DiscountBolt(Bolt):
    outputs = ['solr']

    def initialize(self, stormconf, context):
        pass

    def process(self, tup):
        message = json.loads(tup.values[0])
        product_id = message.get('discount')
        price = message.get('price')
        discount = message.get('discount')
        sale_discount = message.get('sale_discount')

        if all(val is not None for val in [product_id, price, discount, sale_discount]):
            discounted_price = price * (1 - (discount / 100))
            sale_discounted_price = price * (1 - (sale_discount / 100))
            update = {key: 'set' for key in ['discount', 'sale_discount', 'discounted_price', 'sale_discounted_price']}
            doc = {'id': f'doc_{product_id}', 'discount': discount, 'sale_discount': sale_discount,
                   'discounted_price': discounted_price, 'sale_discounted_price': sale_discounted_price}
            self.emit({'doc': doc, 'update': update})
