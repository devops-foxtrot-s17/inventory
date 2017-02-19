from flask import Flask

# Create Flask application
app = Flask(__name__)

@app.route('/')
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
