import os

from app import app, server, utils
from app.redis_inventory import RedisInventory, PRODUCT_ID, LOCATION_ID, USED, NEW, OPEN_BOX, RESTOCK_LEVEL

debug = (os.getenv('DEBUG', 'False') == 'True')
port = os.getenv('PORT', '5000')


def generate_data(to_inventory):
  if len(to_inventory.redis.keys()) <= 1:  # first one is index.
    pid = to_inventory.get_next_product_id()
    to_inventory.put_product(pid, {PRODUCT_ID: pid,
                                   LOCATION_ID: to_inventory.get_next_location_id(),
                                   USED: 1, NEW: 1, OPEN_BOX: 1, RESTOCK_LEVEL: 11})
    pid = to_inventory.get_next_product_id()
    to_inventory.put_product(pid, {PRODUCT_ID: pid,
                                   LOCATION_ID: to_inventory.get_next_location_id(),
                                   USED: 2, NEW: 2, OPEN_BOX: 2, RESTOCK_LEVEL: 22})
    pid = to_inventory.get_next_product_id()
    to_inventory.put_product(pid, {PRODUCT_ID: pid,
                                   LOCATION_ID: to_inventory.get_next_location_id(),
                                   USED: 0, NEW: 5, OPEN_BOX: 3, RESTOCK_LEVEL: 10})


if __name__ == "__main__":
  redis = utils.init_redis_client()
  server.inventory = RedisInventory(redis)
  generate_data(server.inventory)
  app.run(host='0.0.0.0', port=int(port), debug=debug)
