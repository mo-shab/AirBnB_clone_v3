#!/usr/bin/python3
"""Module for Cities Views"""


from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def getCityByStateId(state_id):
    """Route to get state with Id"""

    state = storage.get(State, state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    else:
        return abort(404)
