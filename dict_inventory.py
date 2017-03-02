"""
  Sub class of BaseInventory, implemented with dictionary:
  key: id of the product
  value: the Product object
"""

from base_inventory import BaseInventory
from product import Product, PRODUCT_ID, LOCATION_ID, USED, NEW, OPEN_BOX, RESTOCK_LEVEL


class DictInventory(BaseInventory):

  def __init__(self):
    BaseInventory.__init__(self)
    self.products = {}
    self.test_init()


  def get_product(self, product_id):
    if product_id in self.products:
      return self.products[product_id].data
    else:
      return None


  def get_all(self):
    result = {}
    for k in self.products:
      result[k] = self.products[k].data
    return result


  def put_product(self, id, info):
    info[PRODUCT_ID] = id
    self.products[id] = Product(info)
    return True


  def delete_product(self, product_id):
    if product_id in self.products:
      del self.products[product_id]
      return True
    else:
      raise KeyError('No product with product id %d' % product_id)

  def test_init(self):
    self.products[1] = Product({PRODUCT_ID: 1, LOCATION_ID: 1,
                                USED: 1,NEW: 1, OPEN_BOX: 1, RESTOCK_LEVEL: 11})
    self.products[2] = Product({PRODUCT_ID: 2, LOCATION_ID: 2,
                                USED: 2,NEW: 2, OPEN_BOX: 2, RESTOCK_LEVEL: 22})