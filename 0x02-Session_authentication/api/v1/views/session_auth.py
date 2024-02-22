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
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None:
        return ({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    else:
        for user in users:
            try:
                user.is_valid_password(password)
            except Exception:
                return jsonify({"error": "wrong password"}), 401             
            else:
                from api.v1.app import auth
                session_id = auth.create_session(user.id)
                session_name = getenv("SESSION_NAME")
                user_json = jsonify(user.to_json())
                user_json.set_cookie(session_name, session_id)
                return user_json


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    delete session route
    returns an empty JSON dictionary if successful
    otherwise returns False and abort 404
    """
    from api.v1.app import auth
    destroy = auth.destroy_session(request)
    if destroy is False:
        abort(404)
    return jsonify({}), 200
