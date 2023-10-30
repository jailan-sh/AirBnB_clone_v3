#!/usr/bin/python3
"""
Create a new view for State objects
"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """get all states"""
    new_states = []
    for state in storage.all(State).values():
        new_states.append(state.to_dict())
    return jsonify(new_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ get state by id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_state(state_id):
    """ get state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """create new state"""
    if not request.get_json:
        return make_response('Not a JSON', 400)
    data = request.get_json()
    if 'name' not in data:
        return make_response('Missing name', 400)
    state = State(**data)
    state.save()

    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """update state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(400)
    data = request.get_json()
    if 'name' not in data:
        return make_response('Not a JSON', 400)
    for key, value in data:
        if key is not('id', 'created_at', 'updated_at'):
            setattr(state, key, value)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
