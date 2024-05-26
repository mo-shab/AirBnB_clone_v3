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

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def getCityById(city_id):
    """Route to get City by ID"""

    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        return abort(404)

