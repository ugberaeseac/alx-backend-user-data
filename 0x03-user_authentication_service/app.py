#!/usr/bin/env python3
"""
Basic Flask App
"""


from flask import Flask, jsonify, request, abort
from auth import Auth
from db import DB


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """
    home route
    returns a JSON
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register():
    """
    end-point to register a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    Implement a login route
    respond with a 401 HTTP status if login incorrect
    otherwise create a new session ID and store as a cookie
    """
    email = request.form.get('email')
    password = request.form.get('password')

    user = AUTH.valid_login(email, password)
    if user:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    abort(401)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
