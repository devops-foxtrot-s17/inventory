"""
  Sub class of BaseInventory, implemented with dictionary:
  key: id of the product
  value: the Product object
"""

from base_inventory import BaseInventory
from product import Product


class DictInventory(BaseInventory):

  def __init__(self):
    BaseInventory.__init__(self)
    self.products = {}
    self.test_init()


  def get_product(self, product_id):
    if product_id in self.products:
      return self.products[product_id]
    else:
      return None


  def get_all(self):
    result = {}
    for k in self.products:
      result[k] = self.products[k].__str__()
    return result


  def put_product(self, id, info):
    self.products[id] = Product(id, info['location_id'], info['used'],
                                info['new'], info['open_box'], info['restock_level'])
    return True


  def delete_product(self, product_id):
    if product_id in self.products:
      del self.products[product_id]
      return True
    else:
      raise KeyError('No product with product id %d' % product_id)

  def test_init(self):
    self.products[1] = Product(1,1,1,1,1,4)
    self.products[2] = Product(2,2,2,2,2,7)