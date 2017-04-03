import logging

from flask import Flask

# Create the Flask aoo
app = Flask(__name__)

# Load Configurations
# app.config.from_object('config')
app.config['LOGGING_LEVEL'] = logging.INFO
