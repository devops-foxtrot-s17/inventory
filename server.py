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



    pass



@app.route('/inventory/products/<int: id>', methods=['DELETE'])
def delete_products(id):


    pass

