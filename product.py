PRODUCT_ID = 'product_id'
LOCATION_ID = 'location_id'
USED = 'used'
NEW = 'new'
OPEN_BOX = 'open_box'
RESTOCK_LEVEL = 'restock_level'


class Product:
  def __init__(self, data):
    check_product_id(data[PRODUCT_ID])
    self.data = {PRODUCT_ID: int(data[PRODUCT_ID]),
                 LOCATION_ID: check_location_id(data),
                 USED: check_int_value(data, USED),
                 NEW: check_int_value(data, NEW),
                 OPEN_BOX: check_int_value(data, OPEN_BOX),
                 RESTOCK_LEVEL: check_int_value(data, RESTOCK_LEVEL)}


def check_product_id(value):
  if value is None:
    raise AttributeError('ID can not be empty!')
  elif type(value) is not int:
    raise AttributeError('ID must be integer!')


def check_location_id(data):
  if LOCATION_ID not in data or type(data[LOCATION_ID]) is not int:
    return 0
  else:
    return int(data[LOCATION_ID])


def check_int_value(data, key):
  if key not in data or type(data[key]) is not int:
    return 0
  else:
    return int(data[key])
