import logging
import os

from flask import Flask, jsonify, make_response, request
from dict_inventory import DictInventory
from product import PRODUCT_ID, LOCATION_ID, USED, NEW, OPEN_BOX, RESTOCK_LEVEL

app = Flask(__name__)
app.config['LOGGING_LEVEL'] = logging.INFO

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

# information constants
TYPE = 'type'
QUANTITY = 'quantity'

inventory = DictInventory()

@app.route('/inventory')
def index():
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


@app.route('/inventory/products/<int:id>/update', methods=['PUT'])
def update_to_product(id):
  """ add certain amount to product
  This method will add certain amount to product in the inventory
  (eg. certain amount in new, open box or used.)

  Args:
    id (int): The id of the product to be added to

  Returns:
    response: add successful message with status 200 if succeeded
              or no product found with status 404 if cannot found the product
              or invalid update with status 400 if the update violates any limitation.
  """
  data = inventory.get_product(id)
  if data is not None:
    info = request.get_json()
    if is_valid(info):
      total = data[USED] + data[NEW] + data[OPEN_BOX]

      if info[TYPE] is USED:
        if (total + info[QUANTITY] <= data[RESTOCK_LEVEL]) and (data[USED] + info[QUANTITY] >= 0):
          data[USED] += info[QUANTITY]
          inventory.put_product(id, data)
        else:
          if total + info[QUANTITY] > data[RESTOCK_LEVEL]:
            make_response("Product amount exceed ", HTTP_400_BAD_REQUEST)
          else:
            make_response("Product amount below zero", HTTP_400_BAD_REQUEST)

      if info[TYPE] is NEW:
        if (total + info[QUANTITY] <= data[RESTOCK_LEVEL]) and (data[NEW] + info[QUANTITY] >= 0):
          data[NEW] += info[QUANTITY]
          inventory.put_product(id, data)
        else:
          if total + info[QUANTITY] > data[RESTOCK_LEVEL]:
            make_response("Product amount exceed ", HTTP_400_BAD_REQUEST)
          else:
            make_response("Product amount below zero", HTTP_400_BAD_REQUEST)

      if info[TYPE] is OPEN_BOX:
        if (total + info[QUANTITY] <= data[RESTOCK_LEVEL]) and (data[OPEN_BOX] + info[QUANTITY] >= 0):
          data[OPEN_BOX] += info[QUANTITY]
          inventory.put_product(id, data)
        else:
          if total + info[QUANTITY] > data[RESTOCK_LEVEL]:
            make_response("Product amount exceed ", HTTP_400_BAD_REQUEST)
          else:
            make_response("Product amount below zero", HTTP_400_BAD_REQUEST)

    else:
      make_response("Product data is not valid", HTTP_400_BAD_REQUEST)

    return make_response(jsonify(data), HTTP_200_OK)
  else:
      return make_response("Product not found", HTTP_404_NOT_FOUND)


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
  result = inventory.delete_product(id);
  if result is True:
      return make_response('', HTTP_204_NO_CONTENT)
  else:
      message = {'error' : 'product %s was not found' % id}
      rc = HTTP_404_NOT_FOUND
      return make_response(jsonify(message), rc)


@app.route('/inventory/products', methods= ['POST'])
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
        inventory.put_product(product_id,info={LOCATION_ID: location_id,
                                              RESTOCK_LEVEL: data[RESTOCK_LEVEL]})
        return make_response(jsonify(inventory.get_product(product_id)), HTTP_201_CREATED)
    return make_response('No restock level provided or illegal restock level value', HTTP_400_BAD_REQUEST)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def is_valid(info):
  valid = False
  try:
    type = info[TYPE]
    quantity = info[QUANTITY]
    valid = True
    if not isinstance(quantity, int):
      valid = False
    if type not in ['used', 'new', 'open_box']:
      valid = False
  except KeyError as err:
    app.logger.warn('Missing parameter error: %s', err)
  except TypeError as err:
    app.logger.warn('Invalid Content Type error: %s', err)

  return valid


######################################################################
#   M A I N
######################################################################

if __name__ == "__main__":
    # Pull options from environment
    debug = (os.getenv('DEBUG', 'False') == 'True')
    port = os.getenv('PORT', '5001')
    app.run(host='0.0.0.0', port=int(port), debug=debug)
