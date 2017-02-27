""" Base inventory class

"""
class BaseInventory:

  def __init__(self):
    pass

  def get_product(self, product_id):
    """ Get a product info with id

    Args:
      product_id(int): the id of the product to be retrieved

    Returns:
      the product info
    """
    pass

  def get_all(self):
    """ Get whole list of product

    Returns:
      a copy of the product list
    """
    pass


  def put_product(self, id, info):
    """ Put the product in the inventory
        The product can either exists in the inventory or not.

    Args:
      id(int): the id of the product
      info(dict): the info of the product

    Returns:
      If put success or not.
    """
    pass

  def delete_product(self, product_id):
    """ Delete the product from the inventory

    Args:
      product_id(int): the id of the product to be deleted

    Returns:
      If delete success or not.
    """
    pass