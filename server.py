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