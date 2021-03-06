import json
import os
import unittest

from mock import Mock
from mockredis import mock_redis_client
from redis import ConnectionError, RedisError

from app import utils, server
from app.redis_inventory import USED
from app.utils import connect_to_redis

INVALID_TYPE_USED = 'not_used'


class TestInventoryServer(unittest.TestCase):
  def setUp(self):
    utils.Redis = Mock(return_value=mock_redis_client)
    mock_redis_client.ping = Mock(return_value=True)
    utils.connect_to_redis = Mock(side_effect=connect_to_redis)
    mock_os = Mock()
    mock_os.environ = {}
    utils.os = mock_os

  def tearDown(self):
    utils.os = os

  def test_info_is_valid(self):
    info = {server.TYPE: USED, server.QUANTITY: 20}
    assert utils.is_valid(info) is True

  def test_info_is_invalid_for_illegal_type(self):
    info = {server.TYPE: INVALID_TYPE_USED, server.QUANTITY: 20}
    assert utils.is_valid(info) is False

  def test_info_quantity_not_int(self):
    info = {server.TYPE: USED, server.QUANTITY: '20'}
    assert utils.is_valid(info) is False

  def test_info_missing_key(self):
    info = {server.TYPE: USED}
    assert utils.is_valid(info) is False

  def test_info_not_dict(self):
    info = 'not dictionary'
    assert utils.is_valid(info) is False

  def test_connect_to_redis(self):
    redis = utils.connect_to_redis('', '', '')
    utils.Redis.assert_called_once()
    assert redis is mock_redis_client

  def test_fail_connect_to_redis(self):
    mock_redis_client.ping.side_effect = raise_connection_error
    redis = utils.connect_to_redis('', '', '')
    assert redis is None

  def test_init_redis_client_with_bluemix_redis_bound(self):
    host_name = 'name'
    port = 5006
    password = 'a_password'

    service = json.dumps({'rediscloud':
                            [{'credentials': {'hostname': host_name, 'port': port, 'password': password}}]})
    utils.os.environ = {'VCAP_SERVICES': service}

    utils.init_redis_client()
    utils.connect_to_redis.assert_called_with(host_name, port, password)

  def test_init_redis_client_with_local_server(self):
    utils.init_redis_client()
    utils.connect_to_redis.assert_called_with('127.0.0.1', 6379, None)

  def test_no_redis_on_localhost(self):
    utils.connect_to_redis = Mock(side_effect=side_effect_connect_to_redis)
    utils.init_redis_client()
    utils.connect_to_redis.assert_called_with('redis', 6379, None)

  def test_could_not_find_redis_service(self):
    utils.connect_to_redis = Mock(return_value=None)
    with self.assertRaises(RedisError):
      utils.init_redis_client()


def side_effect_connect_to_redis(host, port, password):
  if host == 'redis':
    return mock_redis_client
  else:
    return None


def raise_connection_error():
  raise ConnectionError
