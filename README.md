# inventory
Inventory keeps track of how many products in warehouse.

### This service provides APIs:
- listing all products
- get single product with id
- update quantity of a product
- create(allocate) the space for new product
- delete a product with id

### For detailed usage guide and full service, go to:
-  https://nyu-devops-s17-inventory.mybluemix.net

### To play with it locally
- clone the repo
- go to the directory: ```cd inventory```
- set up the virtual machine: ```vagrant up```
- ssh into the virtual machine ```vagrant ssh```
- go to the mirror directory of inventory ```cd /vagrant```
- start the server: ```python app/nyu-devops-s17-inventory/server.py```
- go to ```http://0.0.0.0:5000/``` on your local machine.
