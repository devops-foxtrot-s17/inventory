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
    When I visit the "home page"
    Then I should see "Inventory REST API Service"
    Then I should not see "404 Not Found"