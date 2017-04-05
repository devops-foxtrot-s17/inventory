import os

from flask import json
from redis import Redis, ConnectionError, RedisError

import server
from . import app

def is_valid(info):
  valid = False
  try:
    type = info[server.TYPE]
    quantity = info[server.QUANTITY]
    valid = True
    if not isinstance(quantity, int):
      valid = False
    if type not in ['used', 'new', 'open_box']:
      valid = False
  except KeyError as err:
    print('Missing parameter error: %s', err)
  except TypeError as err:
    print('Invalid Content Type error: %s', err)

  return valid


######################################################################
# Connect to Redis and catch connection exceptions#
# This method will work in the following conditions:
#   1) In Bluemix with Redis bound through VCAP_SERVICES
#   2) With Redis running on the local server as with Travis CI
#   3) With Redis --link ed in a Docker container called 'redis'
######################################################################
def init_redis_client():
  redis = None
  # Get the crdentials from the Bluemix environment
  if 'VCAP_SERVICES' in os.environ:
    app.logger.info("Using VCAP_SERVICES...")
    VCAP_SERVICES = os.environ['VCAP_SERVICES']
    services = json.loads(VCAP_SERVICES)
    creds = services['rediscloud'][0]['credentials']
    app.logger.info("Conecting to Redis on host %s port %s" % (creds['hostname'], creds['port']))
    redis = connect_to_redis(creds['hostname'], creds['port'], creds['password'])
  else:
    app.logger.info("VCAP_SERVICES not found, checking localhost for Redis")
    redis = connect_to_redis('127.0.0.1', 6379, None)
    if not redis:
      app.logger.info("No Redis on localhost, using: redis")
      redis = connect_to_redis('redis', 6379, None)

  if not redis:
    # if you end up here, redis instance is down.
    app.logger.error('*** FATAL ERROR: Could not connect to the Redis Service')
    raise RedisError
  return redis


def connect_to_redis(hostname, port, password):
  redis = Redis(host=hostname, port=port, password=password)
  try:
    redis.ping()
  except ConnectionError:
    redis = None
  return redis
