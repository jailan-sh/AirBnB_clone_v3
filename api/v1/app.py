#!/usr/bin/python3
""" app model """

from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_close():
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    my_host = os.getenv('HBNB_API_HOST')
    my_port = os.getenv('HBNB_API_PORT')
    app.run(host=my_host, port=int(my_port), threaded=True)
