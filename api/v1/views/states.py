#!/usr/bin/python3
"""
Create a new view for State objects
"""
from flask import abort, app, jsonify, make_response, request
from models.state import State
from models import storage
from api.v1.views import app_views

@app.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """get all states"""
    new_states = []
    for state in storage.all(State).values():
        new_states.append(state.to_dict())
    return jsonify(new_states)

@app.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ get state by id"""
    state = storage.get(State ,state_id)
    if State.state_id is None:
        abort(404)
    else:
        return jsonify(state.to_dict())
    
@app.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ get state by id"""
    state = storage.get(State ,state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

@app.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """create new state"""
    if not request.get_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    state.save()
    
    return jsonify(state.to_dict()), 201