"""
  Sub class of BaseInventory, implemented with dictionary:
  key: id of the product
  value: the Product object
"""
import os
from flask import json
from redis import Redis
from redis.exceptions import ConnectionError
from base_inventory import BaseInventory
from product import PRODUCT_ID, LOCATION_ID, USED, NEW, OPEN_BOX, RESTOCK_LEVEL

class RedisInventory(BaseInventory):

  def __init__(self,app):
    BaseInventory.__init__(self)
    if 'VCAP_SERVICES' in os.environ:
      app.logger.info("Using VCAP_SERVICES...")
      VCAP_SERVICES = os.environ['VCAP_SERVICES']
      services = json.loads(VCAP_SERVICES)
      creds = services['rediscloud'][0]['credentials']
      app.logger.info("Conecting to Redis on host %s port %s" % (creds['hostname'], creds['port']))
      self.redis = connect_to_redis(creds['hostname'], creds['port'], creds['password'])
    else:
      app.logger.info("VCAP_SERVICES not found, checking localhost for Redis")
      self.redis = connect_to_redis('127.0.0.1', 6379, None)
      if not self.redis:
        app.logger.info("No Redis on localhost, using: redis")
        self.redis = connect_to_redis('redis', 6379, None)

    if not self.redis:
      # if you end up here, redis instance is down.
      app.logger.error('*** FATAL ERROR: Could not connect to the Redis Service')
      exit(1)

    self.next_location_id = 0
    self.test_init()


  def get_product(self, product_id):
    if self.redis.exists(product_id):
      return self.redis.hgetall(product_id)
    else:
      return None


  def get_all(self):
    result = {}
    for key in self.redis.keys():
      if key != 'index':  # filer out our id index
        result[key] = self.redis.hgetall(key)
    return result


  def put_product(self, id, info):
    self.redis.hmset(id, info)
    return True


  def delete_product(self, product_id):
    if self.redis.exists(product_id):
      self.redis.delete(product_id)
      return True
    else:
      return False


  def test_init(self):
    if len(self.redis.keys()) > 1: # first one is index.
      return
    pid = self.get_next_product_id()
    self.put_product(pid, {PRODUCT_ID: pid,
                                LOCATION_ID: self.get_next_location_id(),
                                USED: 1,NEW: 1, OPEN_BOX: 1, RESTOCK_LEVEL: 11})
    pid =  self.get_next_product_id()
    self.put_product(pid,{PRODUCT_ID: pid,
                                LOCATION_ID: self.get_next_location_id(),
                                USED: 2,NEW: 2, OPEN_BOX: 2, RESTOCK_LEVEL: 22})


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


######################################################################
# Connect to Redis and catch connection exceptions
######################################################################
def connect_to_redis(hostname, port, password):
    redis = Redis(host=hostname, port=port, password=password)
    try:
        redis.ping()
    except ConnectionError:
        redis = None
    return redis