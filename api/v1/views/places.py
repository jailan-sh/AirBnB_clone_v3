#!/usr/bin/python3
"""
create a new view for City objects
"""
from flask import abort, app, jsonify, make_response, request
from models.city import City
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.user import User


@app_views.route(
    '/cities/<city_id>/places',
    methods=['GET'],
    strict_slashes=False)
def get_places(city_id):
    """get all places"""
    city = storage.get(City, city_id)
    if city:
        new_places = []
        for place in city.places:
            new_places.append(place.to_dict())
        return jsonify(new_places)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ get place by id"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route(
    '/places/<place_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_place(place_id):
    """ del place by id"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return ({}, 200)
    else:
        abort(404)


@app_views.route(
    '/cities/<city_id>/places',
    methods=['POST'],
    strict_slashes=False)
def create_place(city_id):
    """create new place"""
    city = storage.get(City, city_id)
    if city:
        if not request.get_json:
            abort(400, description='Not a JSON')
        data = request.get_json()
        if 'user_id' not in data:
            abort(400, description='Missing name')
        user_id = data['user_id']
        user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    name = data['name']
    place = Place(city_id=city_id, user_id=user_id, name=name)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """update place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(400)
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Not a JSON')
    for key, value in data:
        if key is not('id', 'user_id', 'city_id', 'created_at', 'updated_at'):
            setattr(place, key, value)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
