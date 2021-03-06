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
  """
    Retrieve a list of Products
    This endpoint will return all Products unless a query parameter is specificed
    ---
    tags:
      - Products
    description: The Products endpoint allows you to query Products
    parameters:
      - name: type
        in: query
        description: The type of Products you are looking for
        required: false
        type: string
    responses:
      200:
        description: An array of Products
        schema:
          type: array
          items:
            schema:
              id: Product
              properties:
                product_id:
                  type: integer
                  description: unique id assigned internally by service
                location_id:
                  type: integer
                  description: unique location id assigned internally by service
                restock_level:
                  type: integer
                  description: max space allocated for the product
                new:
                  type: integer
                  description: quantity of new products
                used:
                  type: integer
                  description: quantity of used products
                open_box:
                  type: integer
                  description: quantity of open_box products
    """
  all_products = inventory.get_all()
  arg = request.args.get(TYPE)

  if arg is None or not arg:
    response = make_response(jsonify(all_products), HTTP_200_OK)

  else:
    arg = arg.lower()
    if arg != OPEN_BOX and arg != NEW and arg != USED:
      response = make_response('Invalid type, must be one of these fields: open_box, new, used', HTTP_400_BAD_REQUEST)
    else:
      l = []
      for product in inventory.get_all():
        if arg in product and int(product[arg]) > 0:
          l.append(product)
      response = make_response(jsonify(l), HTTP_200_OK)

  return response


@app.route('/inventory/products/<int:id>', methods=['GET'])
def get_one_product(id):
  """
    Retrieve a single Product
    This endpoint will return a Product based on it's id
    ---
    tags:
      - Products
    produces:
      - application/json
    parameters:
      - name: id
        in: path
        description: ID of product to retrieve
        type: integer
        required: true
    responses:
      200:
        description: Product returned
        schema:
          id: Product
          properties:
            product_id:
              type: integer
              description: unique id assigned internally by service
            location_id:
              type: integer
              description: unique location id assigned internally by service
            restock_level:
              type: integer
              description: max space allocated for the product
            new:
              type: integer
              description: quantity of new products
            used:
              type: integer
              description: quantity of used products
            open_box:
              type: integer
              description: quantity of open_box products
      404:
        description: Product not found
    """
  product = inventory.get_product(id)
  if product is not None:
    return make_response(jsonify(product), HTTP_200_OK)
  else:
    return make_response("Product not found", HTTP_404_NOT_FOUND)


@app.route('/inventory/products/<int:id>', methods=['PUT'])
def update_product(id):
  """
    Update a Product
    This endpoint will update a Product based on the data that is posted
    ---
    tags:
      - Products
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - name: id
        in: path
        description: ID of product to retrieve
        type: integer
        required: true
      - in: body
        name: body
        schema:
          id: data
          required:
            - type
            - quantity
          properties:
            type:
              type: string
              description: type for the Product
            quantity:
              type: integer
              description: the quantity type you specified
    responses:
      200:
        description: Product returned
        schema:
          id: Product
          properties:
            product_id:
              type: integer
              description: unique id assigned internally by service
            location_id:
              type: integer
              description: unique location id assigned internally by service
            restock_level:
              type: integer
              description: max space allocated for the product
            new:
              type: integer
              description: quantity of new products
            used:
              type: integer
              description: quantity of used products
            open_box:
              type: integer
              description: quantity of open_box products
      400:
        description: Bad Request (the posted data was not valid)
      404:
        description: Product not found
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
  """
  Delete a Product
  This endpoint will delete a Product based the id specified in the path
  ---
  tags:
    - Products
  description: Deletes a Product from the database
  parameters:
    - name: id
      in: path
      description: ID of product to delete
      type: integer
      required: true
  responses:
    204:
      description: Product deleted
  """
  inventory.delete_product(id)
  return make_response('', HTTP_204_NO_CONTENT)


@app.route('/inventory/products', methods=['POST'])
def create_products():
  """
    Creates a Product
    This endpoint will create a Product based the data in the body that is posted
    ---
    tags:
      - Products
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: data
          required:
            - restock_level
          properties:
            restock_level:
              type: integer
              description: the quantity limit for this product
    responses:
      201:
        description: Product created
        schema:
          id: Product
          properties:
            product_id:
              type: integer
              description: unique id assigned internally by service
            location_id:
              type: integer
              description: unique location id assigned internally by service
            restock_level:
              type: integer
              description: max space allocated for the product
            new:
              type: integer
              description: quantity of new products
            used:
              type: integer
              description: quantity of used products
            open_box:
              type: integer
              description: quantity of open_box products
      400:
        description: Bad Request (the posted data was not valid)
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


@app.route('/inventory/products/<int:id>/clear', methods=['PUT'])
def clear_storage(id):
  """
    Clear storage of a product
    This endpoint will clear all the storage of a product
    ---
    tags:
      - Products
    produces:
      - application/json
    parameters:
      - name: id
        in: path
        description: ID of product to retrieve
        type: integer
        required: true
    responses:
      200:
        description: Product returned
        schema:
          id: Product
          properties:
            product_id:
              type: integer
              description: unique id assigned internally by service
            location_id:
              type: integer
              description: unique location id assigned internally by service
            restock_level:
              type: integer
              description: max space allocated for the product
            new:
              type: integer
              description: quantity of new products
            used:
              type: integer
              description: quantity of used products
            open_box:
              type: integer
              description: quantity of open_box products
      404:
        description: Product not found
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
