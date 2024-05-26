#!/usr/bin/python3
"""Module for Cities Views"""


from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """Route to get state with Id"""

    state = storage.get(State, state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    else:
        return abort(404)

@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Get city by ID"""
    try:
        city = storage.get('City', city_id)
        return jsonify(city.to_dict())
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a city by ID"""

    try:
        city = storage.get('City', city_id)
        storage.delete(city)
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
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
def put_city(city_id):
    """Update City object"""

    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'state_id', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
