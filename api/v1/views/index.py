#!/usr/bin/python3
"""Module for The API"""


from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """status route"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def api_stats():
    """stats route"""
    total = {}
    classes = {"Amenity": "amenities",
               "City": "cities",
               "Place": "places",
               "Review": "reviews",
               "State": "states",
               "User": "users"
               }
    for key, value in classes.items():
        total[value] = storage.count(key)
    return jsonify(total)
