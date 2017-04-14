import json

from behave import *

from app import server
from app.redis_inventory import PRODUCT_ID, LOCATION_ID, USED, NEW, OPEN_BOX, RESTOCK_LEVEL


@when(u'I visit "{url}"')
def step_impl(context, url):
  if url == "home page":
    context.resp = context.app.get('/')
  else:
    context.resp = context.app.get(url)
    assert context.resp.status_code == 200


@when(u'I delete "{url}" with id "{id}"')
def step_impl(context, url, id):
  target_url = '/{}/{}'.format(url, id)
  context.resp = context.app.delete(target_url)
  assert context.resp.status_code == 204
  assert context.resp.data is ""


@when(u'I change "{key}" to "{value}"')
def step_impl(context, key, value):
  data = json.loads(context.resp.data)
  data[key] = value
  context.resp.data = json.dumps(data)


@when(u'I update "{url}" with id "{id}"')
def step_impl(context, url, id):
  target_url = '/{}/{}'.format(url, id)
  context.resp = context.app.put(target_url, data=context.resp.data, content_type='application/json')
  assert context.resp.status_code == 200


@then(u'I should see "{message}"')
def step_impl(context, message):
  assert message in context.resp.data


@then(u'I should not see "{message}"')
def step_impl(context, message):
  assert message not in context.resp.data


@given(u'the following products')
def step_impl(context):
  server.inventory.reset()
  for row in context.table:
    server.inventory.put_product(row[PRODUCT_ID], {PRODUCT_ID: row[PRODUCT_ID], LOCATION_ID: row[LOCATION_ID],
                                                   USED: row[USED], NEW: row[NEW], OPEN_BOX: row[OPEN_BOX],
                                                   RESTOCK_LEVEL: row[RESTOCK_LEVEL]})
