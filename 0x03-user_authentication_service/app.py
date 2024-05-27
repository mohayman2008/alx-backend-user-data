#!/usr/bin/env python3
'''Flask app'''
from flask import Flask, jsonify, request

from auth import Auth

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def root() -> str:
    '''Index route'''
    return jsonify({"message": "Bienvenue"})


@app.route("/users/", methods=["POST"], strict_slashes=False)
def register_user() -> str:
    '''Route to register a new user'''
    email = request.form.get("email")
    pasword = request.form.get("password")
    if not email or not pasword:
        return jsonify({
            "error": "Bad request",
            "message": "email and password fields are required"
            }), 400

    try:
        AUTH.register_user(email, pasword)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
