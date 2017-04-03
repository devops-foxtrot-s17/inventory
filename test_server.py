import unittest
import server

from mockredis import mock_redis_client
from redis_inventory import RedisInventory
import json

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

  def test_delete_product(self):
  	resp = self.app.get('/inventory/products')
  	initial_products = json.loads(resp.data)
  	init_count = self.get_product_count()
  	
  	for product in initial_products:
  		resp = self.app.delete('/inventory/products/'+product['product_id'], content_type='application/json')
  		self.assertEqual(resp.status_code, server.HTTP_204_NO_CONTENT)
  		self.assertEqual(len(resp.data), 0)
  		current_count = self.get_product_count()
  		self.assertEqual(current_count, init_count - 1)
  		init_count -= 1

  	final_count = self.get_product_count()
  	self.assertEqual( final_count, 0)

######################################################################
# Utility functions
######################################################################

  def get_product_count(self):
    resp = self.app.get('/inventory/products')
    self.assertEqual(resp.status_code, server.HTTP_200_OK )
    data = json.loads(resp.data)
    return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
	unittest.main()