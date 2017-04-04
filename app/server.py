from flask import jsonify, make_response, request, url_for

import utils
from redis_inventory import LOCATION_ID, NEW, OPEN_BOX, PRODUCT_ID, QUANTITY, RESTOCK_LEVEL, TYPE, USED
from . import app

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

inventory = None


@app.route('/')
def index():
  return app.send_static_file('index.html')


@app.route('/inventory')
def inventory_index():
  """ Intro page of the inventory API
  This method will only return some welcome words.

  Returns:
    response: welcome words in json format and status 200
  """
  welcome_info = {'api': "inventory",
                  'message': "This is the index page of /inventory. "
                             "To see all products, please access /inventory/products"}
  return make_response(jsonify(welcome_info), HTTP_200_OK)


@app.route('/inventory/products', methods=['GET'])
def get_product_list():
  """ Get info about all products
    This method will get the info about all the products

    Returns:
      response: product information(product id, location id, used/new/open_box, total_quantity, restock_level)
      status 200 if succeeded
  """
  all_products = inventory.get_all()
  return make_response(jsonify(all_products), HTTP_200_OK)


@app.route('/inventory/products/<int:id>', methods=['GET'])
def get_one_product(id):
  """ Get info about a specific product
    This method will get the info about an item with it's product id

    Args:
      id (int): The id of the product to be update

    Returns:
      response: product id information(product id, location id, used/new/open_box, total_quantity, restock_level)
      status 200 if succeeded
      or no product found with status 404 if cannot found the product
    """
  product = inventory.get_product(id)
  if product is not None:
    return make_response(jsonify(product), HTTP_200_OK)
  else:
    return make_response("Product not found", HTTP_404_NOT_FOUND)


@app.route('/inventory/products/<int:id>', methods=['PUT'])
def update_product(id):
  """ change product quantity to certain amount
  This method will change product quantity to certain amount in the inventory
  (eg. certain amount in new, open box or used.)

  Args:
    id (int): The id of the product to be added to
    data: {type: [used|new|open_box], quantity: [quantity]}

  Returns:
    response: add successful message with status 200 if succeeded
              or no product found with status 404 if cannot found the product
              or invalid update with status 400 if the update violates any limitation.
  """
  data = inventory.get_product(id)
  info = request.get_json()

  if data is None:
    return make_response("Product not found", HTTP_404_NOT_FOUND)

  if not utils.is_valid(info):
    return make_response("Product data is not valid", HTTP_400_BAD_REQUEST)

  total = int(data[USED]) + int(data[NEW]) + int(data[OPEN_BOX])
  prod_type = info[TYPE]

  if total - int(data[prod_type]) + int(info[QUANTITY]) > int(data[RESTOCK_LEVEL]):
    return make_response("Product amount exceed restock level", HTTP_400_BAD_REQUEST)

  if int(info[QUANTITY]) < 0:
    return make_response("Product amount below zero", HTTP_400_BAD_REQUEST)

  data[prod_type] = int(info[QUANTITY])
  inventory.put_product(id, data)
  return make_response(jsonify(data), HTTP_200_OK)


@app.route('/inventory/products/<int:id>', methods=['DELETE'])
def delete_product(id):
  """ delete a product by id
    This method will delete an existing product from inventory
    or simply will do nothing if it does not exist.

    Args:
      id (int): The id of the product to be deleted

    Returns:
      response: Delete successful message with status 204 if product exist and is deleted
                or no product found with status 404 if product does not exist
 """
  inventory.delete_product(id)
  return make_response('', HTTP_204_NO_CONTENT)


@app.route('/inventory/products', methods=['POST'])
def create_products():
  """ create a product with restock level.
  This method will create a storage for a new product

  Args: data with restock_level provided.

  Returns:

    response: create successful message with status 201 if succeeded,
              the auto assigned product id and location id should also be presented
              or invalid create with status 400 if the create request violates any limitation
  """
  data = request.get_json()
  if RESTOCK_LEVEL in data and type(data[RESTOCK_LEVEL]) is int and data[RESTOCK_LEVEL] > 0:
    product_id = inventory.get_next_product_id()
    location_id = inventory.get_next_location_id()
    inventory.put_product(product_id, info={LOCATION_ID: location_id,
                                            NEW: 0,
                                            USED: 0,
                                            OPEN_BOX: 0,
                                            RESTOCK_LEVEL: data[RESTOCK_LEVEL],
                                            PRODUCT_ID: product_id
                                            })
    response = make_response(jsonify(inventory.get_product(product_id)), HTTP_201_CREATED)
    response.headers['Location'] = url_for('get_one_product', id=product_id)
  else:
    response = make_response('No restock level provided or illegal restock level value', HTTP_400_BAD_REQUEST)
  return response


@app.route('/inventory/product', methods=['GET'])
def get_products_with_type():
  """ Gets products with quantity of type larger than 0


  Returns:
    response: add successful message with status 200 if succeeded
              or no type provided or found 400 bad request.
  """
  l = []
  arg = request.args.get(TYPE)

  if arg is None or not arg:
    response = make_response('Invalid argument, need the type of product as one of the fields: open_box, new, used',
                             HTTP_400_BAD_REQUEST)
    return response
  arg = arg.lower()

  if arg != OPEN_BOX and arg != NEW and arg != USED:
    response = make_response('Invalid type, must be one of these fields: open_box, new, used', HTTP_400_BAD_REQUEST)
    return response

  for product in inventory.get_all():
    if arg in product and int(product[arg]) > 0:
      l.append(product)
  response = make_response(jsonify(l), HTTP_200_OK)
  return response


@app.route('/inventory/products/<int:id>/clear', methods=['PUT'])
def clear_storage(id):
  """ Clears a product out of inventory
      (total quantity -> 0)

  Args:
    id (int): The id of the product
  Returns:
    response: add successful message with status 200 if succeeded
              or no product found with status 404 if cannot found the product
  """
  data = inventory.get_product(id)
  if data is None:
    return make_response("Product not found", HTTP_404_NOT_FOUND)
  else:
    data[USED] = 0
    data[NEW] = 0
    data[OPEN_BOX] = 0

    inventory.put_product(id, data)
    return make_response(jsonify(data), HTTP_200_OK)
