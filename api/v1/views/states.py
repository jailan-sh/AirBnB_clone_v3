#!/usr/bin/python3
"""
Create a new view for State objects
"""
from flask import abort, app, jsonify, make_response, request
import models
from models.state import State, state
from models.base_model import BaseModel, Base
from models import storage

@app.route('/states', methods=['GET'], strict_slashes=False)
def GET_all_states():
    """get all states"""
    new_states = []
    for state in storage.all(State).values():
        new_states.append(state.to_dict())
    return jsonify(new_states)

@app.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def GET_state(state_id):
    """ get state by id"""
    state = storage.get(State ,state_id)
    if State.state_id is None:
        abort(404)
    else:
        return jsonify(state.to_dict())
    
@app.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def DELETE_state(state_id):
    """ get state by id"""
    state = storage.get(State ,state_id)
    if State.state_id is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

@app.route('/states', methods=['POST'], strict_slashes=False)
def POST_state(states_name):
    if not request.get_json or not 'states_name' in request.get_json:
        abort(400, 'Not a JSON')
    elif  not 'states_name' in request.get_json:
        abort(400, 'Missing name')
    else:
        