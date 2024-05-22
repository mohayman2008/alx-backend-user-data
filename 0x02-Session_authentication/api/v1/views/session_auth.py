#!/usr/bin/env python3
'''Module of Session Authentication views'''
from os import getenv

from flask import abort, jsonify, request

from . import app_views
from models.user import User

SESSION_NAME = getenv("SESSION_NAME", "_my_session_id")


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login/
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if email or password is missing
      - 404 if no user associated with "email" was found
      - 401 if password is invalid
    """
    email = request.form.get("email")
    if not email:
        return jsonify({'error': "email missing"}), 400

    password = request.form.get("password")
    if not password:
        return jsonify({'error': "password missing"}), 400

    users = User.search({"email": email})
    if not len(users):
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({'error': "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v1/auth_session/logout/
    JSON body:
      - email
      - password
    Return:
      - Empty dictionary JSON represented, status = 200
      - 404 if session cookie wasn't sent in the request or is invalid
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
