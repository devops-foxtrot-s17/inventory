from behave import *

from app import server
from app.redis_inventory import PRODUCT_ID, LOCATION_ID, USED, NEW, OPEN_BOX, RESTOCK_LEVEL


@when(u'I visit the "home page"')
def step_impl(context):
  context.resp = context.app.get('/')


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
