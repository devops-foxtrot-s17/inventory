import unittest
import server

from mockredis import mock_redis_client
from redis_inventory import RedisInventory

######################################################################
#  T E S T   C A S E S
######################################################################
class TestInventoryServer(unittest.TestCase):

  def setUp(self):
    redis = mock_redis_client()
    server.inventory = RedisInventory(redis)
    self.app = server.app.test_client()

  def test_index(self):
    resp = self.app.get('/')
    self.assertEqual(resp.status_code, server.HTTP_200_OK)
    self.assertTrue('Inventory REST API Service' in resp.data)

  def test_inventory_index(self):
    resp = self.app.get('/inventory')
    self.assertEqual(resp.status_code, server.HTTP_200_OK)
    self.assertTrue('index page of /inventory' in resp.data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()