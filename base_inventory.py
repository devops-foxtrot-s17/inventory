""" Base inventory class

"""
class BaseInventory:

  def get_product(self, product_id):
    """ Get a product info with id

    Args:
      product_id(int): the id of the product to be retrieved

    Returns:
      the product info in dict format
    """
    pass

  def get_all(self):
    """ Get whole list of product

    Returns:
      a copy of the product list
    """
    pass


  def put_product(self, product_id, product_info):
    """ Put the product in the inventory
        The product can either exists in the inventory or not.

    Args:
      product_id(int): the id of the product
      product_info(dict): the info of the product

    Returns:
      If put success or not.
    """
    pass