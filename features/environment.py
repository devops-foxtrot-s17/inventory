from mockredis import mock_redis_client

from app import server
from app.redis_inventory import RedisInventory


def before_all(context):
  redis = mock_redis_client()
  server.inventory = RedisInventory(redis)
  context.app = server.app.test_client()
  context.server = server
