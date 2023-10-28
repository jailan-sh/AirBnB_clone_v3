#!/usr/bin/python3
""" app model """

from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

@app.teardown_appcontext
def tear_close():
    """closes the storage on teardown"""
    storage.close()

if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
