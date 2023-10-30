#!/usr/bin/python3
"""handelling RESTFUL API from amenity"""

from flask import make_response, jsonify, abort, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """all amenities """
    amenity = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return make_response(jsonify(amenity), 200)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """get one """
    amenity = storage.get(Amenity, amenity_id)
    return make_response(jsonify(amenity.to_dict()),
                         200) if amenity else abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """remove amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """post amenity"""
    amenity = request.get_json()
    if not amenity:
        return make_response("Not a JSON", 400)
    if not amenity.get('name'):
        return make_response("Missing name", 400)
    new_amenity = Amenity(**amenity)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """update """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amen= request.get_json()
    if not amen:
        return make_response("Not a JSON", 400)
    setattr(amenity, 'name', amen.get('name'))
    storage.save()
    return make_response(amenity.to_dict(), 200)
