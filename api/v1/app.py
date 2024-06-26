#!/usr/bin/python3
"""Module for The API"""

from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask_cors import CORS


app = Flask(__name__)


cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """teardown function"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Page not found"""
    response = {
        "error": "Not found"
    }
    return jsonify(response), 404


if __name__ == "__main__":
    """Main function"""
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = getenv('HBNB_API_PORT', '5000')
    app.run(host=HOST, port=PORT, threaded=True)
