#!/usr/bin/python3
"""Modele for Places Views"""

from flask import abort, jsonify, request
from models import storage
from models import City, Place, User
from api.v1.views import app_views

@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 slash_slashes=False)
def getPlaceByCityId(city_id):
    """Route to get all places by city id"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def getPlaceByID(place_id):
    """Route to get place by id"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlaceById(place_id):
    """Route to delete place by id"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def postPlace(city_id):
    """Route to post a new place"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.content_type != 'application/json':
        return jsonify({'error': 'Not a JSON'}), 400
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, kwargs['user_id'])
    if user is None:
        abort(404)
    if 'name' not in kwargs:
        return jsonify({'error': 'Missing name'}), 400
    kwargs['city_id'] = city_id
    place = Place(**kwargs)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 slash_slashes=False)
def putPlace(place_id):
    """Route to update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.content_type != 'application/json':
        return jsonify({'error': 'Not a JSON'}), 400
    kwargs = request.get_json()
    if not kwargs:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in kwargs.items():
        if key not in ['id', 'user_id', 'city_id', 'created at',
                           'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
