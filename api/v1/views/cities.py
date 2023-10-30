#!/usr/bin/python3
"""
create a new view for City objects
"""
from flask import abort, app, jsonify, make_response, request
from models.city import City
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False)
def get_cities(state_id):
    """get all cities"""
    state = storage.get(State, state_id)
    if state:
        new_cities = []
        for city in state.cities:
            new_cities.append(city.to_dict())
        return jsonify(new_cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ get city by id"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route(
    '/cities/<city_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_city(city_id):
    """ get city by id"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """create new city"""
    if not request.get_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, description='Missing name')
    state = storage.get(State, state_id)
    if state :
        data['state_id'] = state_id
        city = City(**data)
        city.save()
    else:
        abort(404)

    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """update city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(400)
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Not a JSON')
    for key, value in data:
        if key is not('id', 'state_id', 'created_at', 'updated_at'):
            setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
