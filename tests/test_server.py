import json
import unittest

from mockredis import mock_redis_client

from app import server
from app.redis_inventory import RedisInventory

PRODUCT_ID = 'product_id'
LOCATION_ID = 'location_id'
USED = 'used'
NEW = 'new'
OPEN_BOX = 'open_box'
RESTOCK_LEVEL = 'restock_level'
TYPE = 'type'
QUANTITY = 'quantity'


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
      resp = self.app.delete('/inventory/products/' + product['product_id'], content_type='application/json')
      self.assertEqual(resp.status_code, server.HTTP_204_NO_CONTENT)
      self.assertEqual(len(resp.data), 0)
      current_count = self.get_product_count()
      self.assertEqual(current_count, init_count - 1)
      init_count -= 1

    final_count = self.get_product_count()
    self.assertEqual(final_count, 0)

  def test_product_create(self):
    initial_count = self.get_product_count()
    new_product = {RESTOCK_LEVEL: 20}
    data = json.dumps(new_product)
    resp = self.app.post('/inventory/products', data=data, content_type='application/json')
    self.assertEqual(resp.status_code, server.HTTP_201_CREATED)
    location = resp.headers.get('Location', None)
    self.assertTrue(location != None)
    new_json = json.loads(resp.data)
    self.assertEqual(int(new_json[RESTOCK_LEVEL]), 20)
    resp = self.app.get('/inventory/products')
    data = json.loads(resp.data)
    self.assertEqual(resp.status_code, server.HTTP_200_OK)
    self.assertEqual(len(data), initial_count + 1)
    self.assertIn(new_json, data)

  def test_product_create_with_no_data(self):
    resp = self.app.post('inventory/products', content_type='application/json')
    self.assertEqual(resp.status_code, server.HTTP_400_BAD_REQUEST)

  def test_product_create_with_null_data(self):
    resp = self.app.post('inventory/products', data=None, content_type='application/json')
    self.assertEqual(resp.status_code, server.HTTP_400_BAD_REQUEST)

  def test_product_create_with_fieldless_data(self):
    product = {}
    data = json.dumps(product)
    resp = self.app.post('inventory/products', data=data, content_type='application/json')
    self.assertEqual(resp.status_code, server.HTTP_400_BAD_REQUEST)

  def test_list_inventory(self):
    resp = self.app.get('/inventory/products')
    self.assertEqual(resp.status_code, server.HTTP_200_OK)

  def test_get_pet(self):
    resp = self.app.get('/inventory/products')
    self.assertEqual(resp.status_code, server.HTTP_200_OK)
    data = json.loads(resp.data)
    self.assertEqual(int(data[0][RESTOCK_LEVEL].encode("utf-8")), 11)

  def test_get_pet_not_found(self):
    resp = self.app.get('/inventory/products/0')
    self.assertEqual(resp.status_code, server.HTTP_404_NOT_FOUND)

  ######################################################################
  # Utility functions
  ######################################################################
  def get_product_count(self):
    resp = self.app.get('/inventory/products')
    self.assertEqual(resp.status_code, server.HTTP_200_OK)
    data = json.loads(resp.data)
    return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
  unittest.main()