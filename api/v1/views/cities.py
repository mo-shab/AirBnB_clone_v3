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

@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteCityId(city_id):
    """Route to delete city bi ID"""
    city = storage.get(City, city_id)
    if city:
        storage .delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def postCityByStateId(state_id):
    """Create New city in a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    kwargs = request.get_json()
    kwargs['state_id'] = state_id
    city = City(**kwargs)
    city.save()
    return jsonify(city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'],
                    strict_slashes=False)
def putCity(city_id):
    """Update a city by ID"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
