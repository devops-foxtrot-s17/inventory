import os

from app import app, server, utils
from redis_inventory import RedisInventory

debug = (os.getenv('DEBUG', 'False') == 'True')
port = os.getenv('PORT', '5001')

if __name__ == "__main__":
  redis = utils.init_redis_client()
  server.inventory = RedisInventory(redis)
  app.run(host='0.0.0.0', port=int(port), debug=debug)
