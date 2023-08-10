#!/usr/bin/python3
"""Impliment a log in endpoint"""
from api.v1.views import app_views
from flask import jsonify, request, make_response
from models.user import User
import os

SESSION_NAME = os.getenv('SESSION_NAME')


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def handle_login() -> str:
    """Get credentials from request form and return a session id in json
    if the user exists"""
    email: str = request.form.get('email')
    password: str = request.form.get('password')

    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    elif password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        user = User.search({'email': email})[0]
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = str(auth.create_session(user.id))
            print(type(session_id))
            response = make_response(user.to_json())
            response.set_cookie(SESSION_NAME, session_id)
            return response
        else:
            return jsonify({"error": "wrong password"}), 401
    except IndexError:
        return jsonify({"error": "no user found for this email"})


@app_views.route('auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def delete_session():
    """Delete a session"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({})
    else:
        abort(404)
