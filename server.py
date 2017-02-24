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

  pass

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
