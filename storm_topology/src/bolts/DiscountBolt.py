from streamparse import Bolt

class DiscountBolt(Bolt):
    def initialize(self, stormconf, context):
        pass

    def process(self, tup):
        product_id, price = tup.values[0]
        message = json.loads(tup.values[1])
        discount = message.get('discount')
        sale_discount = message.get('sale_discount')
        if all(val is not None for val in [product_id, price, discount, sale_discount]):
            discounted_price = price * (1 - (discount / 100))
            sale_discounted_price = price * (1 - (sale_discount / 100))
            update = {key: 'set' for key in ['discount', 'sale_discount', 'discounted_price', 'sale_discounted_price']}
            doc = {'id': f'doc_{product_id}', 'discount': discount, 'sale_discount': sale_discount,
                   'discounted_price': discounted_price, 'sale_discounted_price': sale_discounted_price}
            self.emit({'product_id': product_id, 'doc': doc, 'update': update})
