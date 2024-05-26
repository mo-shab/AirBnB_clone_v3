#!/usr/bin/python3
"""Module for States Views"""


from flask import abort, jsonify, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', strict_slacshes=False)
def get_all_states():
    """Route to get all states"""

    states = storage.all(State)
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def getStateId(state_id):
    """Route to get state with Id"""

    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404)


@app_views.route('/states/<state_id>', methodes=['DELETE'],
                 strict_slashes=False)
def getStateId(state_id):
    """Route to delete state with Id"""

    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)

@app_views.route('/states', methodes=['POST'],
                 strict_slashes=False)
def postState():
    """Route to post a new state"""

    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    new_state = State(**request.get_json())
    new_state.save()
    return jsonify(new_state.to_dict()), 200

@app_views.route('/states/<state_id>', methodes=['PUT'],
                 strict_slashes=False)
def putState(state_id):
    """Route to update a state"""

    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
