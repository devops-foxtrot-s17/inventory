Feature: The pet store service back-end
  As a Pet Store Owner
  I need a RESTful catalog service
  So that I can keep track of all my pets

  Background:
    Given the following products
      | product_id | location_id | used | open_box | new | restock_level |
      | 11         | 122         | 11   | 21       | 31  | 100           |
      | 21         | 222         | 12   | 22       | 32  | 100           |
      | 31         | 322         | 13   | 23       | 33  | 100           |

  Scenario: The server is running
    When I visit "home page"
    Then I should see "Inventory REST API Service"
    Then I should not see "404 Not Found"

  Scenario: Accessing the inventory
    When I visit "inventory"
    Then I should see "index page of /inventory"
    Then I should not see "404 Not Found"

  Scenario: List all products
    When I visit "inventory/products"
    Then I should see "11"
    And I should see "21"
    And I should see "31"

  Scenario: List a product
    When I retrieve product with id "11"
    Then I should see "11"
    And I should have "location_id" equals to "122"
    And I should not see "404 Not Found"

  Scenario: Update a product
    When I retrieve product with id "11"
    And I change "used" to "23"
    And I update product with id "11"
    Then I should have "used" equals to "23"

  Scenario: Create a product
    When I create a product with restock level "111"
    Then I should not have "product_id" equals to "11"
    And I should not have "product_id" equals to "21"
    And I should not have "product_id" equals to "31"
