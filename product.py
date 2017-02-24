
class Product:

    def __init__(self, product_id, location_id, used, new, open_box, restock_level):

        if product_id is None:
            raise AttributeError('ID can not be empty!')
        elif product_id is not int:
            raise AttributeError('ID must be integer!')
        else:
            self.product_id = int(product_id)

        if location_id is None or location_id is not int:
            self.location_id = 0
        else:
            self.location_id = int(location_id)

        if used is None or used is not int:
            self.used = 0
        else:
            self.used = int(used)

        if new is None or new is not int:
            self.new = 0
        else:
            self.new = int(new)

        if open_box is None or open_box is not int:
            self.open_box = 0
        else:
            self.open_box = int(open_box)

        if restock_level is None or restock_level is not int:
            self.restock_level = 0
        else:
            self.restock_level = int(restock_level)

    # To have a nice explanatory version when the product is printed
    def __str__(self):
        return 'Product id: ' + str(self.product_id) + ', location: ' + str(self.location_id) + ', # used: ' + \
               str(self.used) + ', # new: ' + str(self.new) + ', # open box: ' + str(self.open_box) + \
                ', # total: ' + str(self.total_quantity) + ', restock at: ' + str(self.restock_level)

