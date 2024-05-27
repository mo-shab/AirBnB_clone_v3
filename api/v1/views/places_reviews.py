#!/usr/bin/python3
"""Modele for Review Views"""

from flask import Flask, abort, jsonify, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def getReviewByPlaceId(place_id):
    """Route to get all reviews by place id"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def getReviewById(review_id):
    """Route to get review by id"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteReviewById(review_id):
    """Route to delete review by id"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def postReviewByPlaceId(place_id):
    """Route to post a new review"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.content_type != 'application/json':
        return jsonify({'error': 'Not a JSON'}), 400
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        return jsonify({'error': 'Missing user_id'}), 400
    if 'text' not in kwargs:
        return jsonify({'error': 'Missing text'}), 400
    user = storage.get(User, kwargs['user_id'])
    if user is None:
        abort(404)
    kwargs['place_id'] = place_id
    review = Review(**kwargs)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def putReview(review_id):
    """Route to update a review by ID"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.content_type != 'application/json':
        return jsonify({'error': 'Not a JSON'}), 400
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    kwargs = request.get_json()
    for key, value in kwargs.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
