#!/usr/bin/env python3
'''Flask app'''
from flask import abort, Flask, jsonify, redirect, request

from auth import Auth

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def root() -> str:
    '''Index route'''
    return jsonify({"message": "Bienvenue"})


@app.route("/users/", methods=["POST"], strict_slashes=False)
def users() -> str:
    '''Route to register a new user'''
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return jsonify({
            "error": "Bad request",
            "message": "email and password fields are required"
            }), 400

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions/", methods=["POST"], strict_slashes=False)
def login() -> str:
    '''Route for user login'''
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return jsonify({
            "error": "Bad request",
            "message": "email and password fields are required"
            }), 400

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)

    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions/", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    '''Route for user logout'''
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
