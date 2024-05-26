#!/usr/bin/python3
"""Module for States Views"""

from flask import abort, jsonify
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


@app_views.route('/states/<state_id>', methodes=['DELETE'], strict_slashes=False)
def getStateId(state_id):
    """Route to delete state with Id"""

    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)