import logging

from flask import Flask
from flasgger import Swagger

# Create the Flask aoo
app = Flask(__name__)

# Load Configurations
# app.config.from_object('config')
app.config['LOGGING_LEVEL'] = logging.INFO
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "specs": [
        {
            "version": "1.0.0",
            "title": "Inventory ",
            "description": "This is the inventory api.",
            "endpoint": 'v1_spec',
            "route": '/v1/spec'
        }
    ]
}

# Initialize Swagger after configuring it
Swagger(app)

import server
import utils
import redis_inventory