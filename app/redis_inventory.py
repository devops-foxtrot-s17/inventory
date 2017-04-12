"""
  Sub class of BaseInventory, implemented with dictionary:
  key: id of the product
  value: the Product object
"""
from base_inventory import BaseInventory

PRODUCT_ID = 'product_id'
LOCATION_ID = 'location_id'
USED = 'used'
NEW = 'new'
OPEN_BOX = 'open_box'
RESTOCK_LEVEL = 'restock_level'
TYPE = 'type'
QUANTITY = 'quantity'


class RedisInventory(BaseInventory):
  def __init__(self, redis):
    BaseInventory.__init__(self)
    self.redis = redis
    self.next_location_id = 0

  def get_product(self, product_id):
    if self.redis.exists(product_id):
      return self.redis.hgetall(product_id)
    else:
      return None

  def get_all(self):
    result = []
    for key in self.redis.keys():
      if key != 'index':  # filer out our id index
        result.append(self.redis.hgetall(key))
    return result

  def put_product(self, id, info):
    self.redis.hmset(id, info)
    return True

  def delete_product(self, product_id):
    if self.redis.exists(product_id):
      self.redis.delete(product_id)

  def reset(self):
    self.redis.flushdb()

  ##################################################################
  # helper methods to get ids.
  ##################################################################
  def get_next_product_id(self):
    self.redis.incr('index')
    index = self.redis.get('index')
    return index

  def get_next_location_id(self):
    self.next_location_id += 1
    return self.next_location_id - 1
