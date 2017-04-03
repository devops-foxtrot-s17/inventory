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
    self.test_init()

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

  def test_init(self):
    if len(self.redis.keys()) > 1:  # first one is index.
      return
    pid = self.get_next_product_id()
    self.put_product(pid, {PRODUCT_ID: pid,
                           LOCATION_ID: self.get_next_location_id(),
                           USED: 1, NEW: 1, OPEN_BOX: 1, RESTOCK_LEVEL: 11})
    pid = self.get_next_product_id()
    self.put_product(pid, {PRODUCT_ID: pid,
                           LOCATION_ID: self.get_next_location_id(),
                           USED: 2, NEW: 2, OPEN_BOX: 2, RESTOCK_LEVEL: 22})
    pid = self.get_next_product_id()
    self.put_product(pid, {PRODUCT_ID: pid,
                           LOCATION_ID: self.get_next_location_id(),
                           USED: 0, NEW: 5, OPEN_BOX: 3, RESTOCK_LEVEL: 10})

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
