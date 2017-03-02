import logging
import os

from flask import Flask, jsonify, make_response, request

from dict_inventory import DictInventory

app = Flask(__name__)
app.config['LOGGING_LEVEL'] = logging.INFO

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409


inventory = DictInventory()

@app.route('/inventory')
def index():
  """ Intro page of the inventory API

  This method will only return some welcome words.

  Returns:
    response: welcome words in json format and status 200

  Todo:
    * Finish the implementations.
    * Write the tests for this.

  """
  welcome_info = {'api': "inventory",
                  'message': "This is the index page of /inventory. "
                             "To see all products, please access /inventory/products"}
  return make_response(jsonify(welcome_info), HTTP_200_OK)

@app.route('/inventory/products', methods=['GET'])
def get_product_list():
  """ Get info about all products

    This method will get the info about all the products

    Args:
      no arguments

    Returns:
      response: product information(product id, location id, used/new/open_box, total_quantity, restock_level)
      status 200 if succeeded

    Todo:
      * Finish the implementations.
      * Write the tests for this.

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

    Todo:
      * Finish the implementations.
      * Write the tests for this.
    """
  product = inventory.get_product(id)
  if product is not None:
    return make_response(product.__str__(), HTTP_200_OK)
  else:
    return make_response("Product not found", HTTP_404_NOT_FOUND)



@app.route('/inventory/products/<int:id>/add', methods=['PUT'])
def add_to_product(id):
  """ add certain amount to product

  This method will add certain amount to product in the inventory
  (eg. certain amount in new, open box or used.)

  Args:
    id (int): The id of the product to be added to

  Returns:
    response: add successful message with status 200 if succeeded
              or no product found with status 404 if cannot found the product
              or invalid update with status 400 if the update violates any limitation.

  Todo:
    * Finish the implementations.
    * Write the tests for this.

  """
  product = inventory.get_product(id)
  if product is not None:
      info = request.get_json()
      if is_valid(info):
         inventory.put_product(id, info)
      else:
          make_response("Product data is not valid", HTTP_400_BAD_REQUEST)
      return make_response(product.__str__(), HTTP_200_OK)
  else:
      return make_response("Product not found", HTTP_404_NOT_FOUND)



@app.route('/inventory/products/<int:id>/remove', methods=['PUT'])
def remove_from_product(id):
  """ remove certain amount from product

  This method will remove certain amount from product
  (eg. amount in new, open box or used.)

  Args:
    id (int): The id of the product to be removed from

  Returns:
    response: remove successful message with status 200 if succeeded
              or no product found with status 404 if cannot found the product
              or invalid update with status 400 if the update violates any limitation.

  Todo:
    * Finish the implementations.
    * Write the tests for this.

  """
  pass

@app.route('/inventory/products/<int:id>', methods=['DELETE'])
def delete_product(id):
  """
    This method will delete an existing product from inventory
    or simply will do nothing if it does not exist.

    Args:
      id (int): The id of the product to be deleted

    Returns:
      response: Delete successful message with status 200 if product exist and is deleted
                or no product found with status 404 if product does not exist
                or invalid update with status 400 if the amount in inventory is less than
                amount to be deleted

    Todo:
     * Finish the implementation
     * Write test cases

 """
  result = inventory.delete_product(id);
  if result is True:
      return make_response('', HTTP_204_NO_CONTENT)
  else:
      message = {'error' : 'product %s was not found' % id}
      rc = HTTP_404_NOT_FOUND
      return make_response(jsonify(message), rc)


@app.route('/inventory/products/', methods= ['POST'])
def create_products():
    """

    This method will create a storage for a new product

    Args:

    Returns:

      response: create successful message with status 201 if succeeded, the auto assigned product id should also be presented
                or invalid update with status 400 if the create request violates any limitation
                or conflict update with status 409 there is a identical product already in the data.

    Todo:
      * Finish the implementations.
      * Write the tests for this.

    """
    pass

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def is_valid(info):
    valid = False
    try:
        product_id = info['product_id']
        location_id = info['location_id']
        used = info['used']
        new = info['new']
        open_box = info['open_box']
        restock_level = info['restock_level']
        valid = True
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
    port = os.getenv('PORT', '5000')
    app.run(host='0.0.0.0', port=int(port), debug=debug)
