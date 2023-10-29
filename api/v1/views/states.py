#!/usr/bin/python3
"""
Create a new view for State objects
"""
from flask import abort, app, jsonify, make_response, request
from models.state import State
from models import storage
from api.v1.views import app_views


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
        abort(400, description='Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, description='Missing name')
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
        abort(400, 'Not a JSON')
    for key, value in data:
        if key is not('id', 'created_at', 'updated_at'):
            setattr(state, key, value)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
