#!/usr/bin/python3
"""wed api"""
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', method=['GET'], strict_slashes=False)
def status_f():
    """return status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', method=['GET'], strict_slashes=False)
def total():
    """count objects"""
    all_obj = {"amenities": storage.count("Amenity"),
               "cities": storage.count("City"),
               "places": storage.count("Place"),
               "reviews": storage.count("Review"),
               "states": storage.count("State"),
               "users": storage.count("User")
               }
    return jsonify(all_obj)
