#!/usr/bin/python3
"""Module for States Views"""


from flask import abort, jsonify, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """Route to get all states"""

    states = storage.all(State).values()
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

@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def postState():
    """Route to post a new state"""

    if request.content_type != 'application/json':
        return jsonify({'error': 'Not a JSON'}), 404
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    kwargs = request.get_json()
    if 'name' not in kwargs:
        return jsonify({'error': 'Missing name'}), 400
    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 200

@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteStateId(state_id):
    """Route to delete state with Id"""

    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/states/<state_id>', methods=['PUT'],
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
