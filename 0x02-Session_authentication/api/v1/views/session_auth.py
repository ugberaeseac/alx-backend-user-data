#!/usr/bin/env python3
"""
Flask view that handles all routes
for Session Authentication
"""


from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session() -> str:
    """
    auth session login route
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return ({"error": "email missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_name = getenv('SESSION_NAME')
            session_id = auth.create_session(user.id)
            user_json = jsonify(user.to_json())
            user_json.set_cookie(session_name, session_id)
            return user.json
        else:
            return jsonify({'error': 'wrong password'}), 401
