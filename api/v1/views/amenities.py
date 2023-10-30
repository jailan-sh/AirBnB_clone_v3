#!/usr/bin/python3
"""handelling RESTFUL API from amenity"""

from flask import Flask, make_response, jsonify, abort, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', method=['GET'], strict_slashes=False)
def get_all_amenity():
    """to get all amenity"""
    all_objects = storage.all(Amenity).values()
    amenities = []
    for one in all_objects:
        amenities.append(one.to_dict())
        return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', method=['GET'],
                 strict_slashes=False)
def one_amenity(amenity_id):
    """return one object"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', method=['DELETE'],
                 strict_slashes=False)
def remove(amenity_id):
    """remove item"""
    out = storage.get(Amenity, amenity_id)
    if not out:
        abort(404)
    else:
        storage.delete(out)
        storage.save()
    return make_response(jsonify({}, 200))


@app_views.route('/amenities', method=['POST'], strict_slashes=False)
def add():
    """add amenity object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    addition = Amenity(**data)
    addition.save()
    return make_response(jsonify(addition.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def edit_amenity(amenity_id):
    """update amenity"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
