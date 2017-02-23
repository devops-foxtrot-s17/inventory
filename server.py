from flask import Flask

# Create Flask application
app = Flask(__name__)

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
  pass

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


@app.route('/inventory/products/<int:id>', methods=['GET'])
def get_one_product(id):
  """ Get info about a specific product

    This method will get the info about an item with it's product id

    Args:
      id (int): The id of the product to be update

    Returns:
      response: product id information(product id, location id, used/new/open_box, total_quantity, restock_level)
      status 200 if succeeded

    Todo:
      * Finish the implementations.
      * Write the tests for this.

    """



@app.route('/inventory/products/<int:id>', methods=['PUT'])
def update_product(id):
  """ Update info about a product

  This method will update the info about a product
  (eg. amount of new, open box or used.)

  Args:
    id (string): The id of the product to be update

  Returns:
    response: update successful message with status 200 if succeeded
              or no product found with status 404 if cannot found the product
              or invalid update with status 400 if the update violates any limitation.

  Todo:
    * Finish the implementations.
    * Write the tests for this.

  """
  pass
