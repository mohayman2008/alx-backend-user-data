#!/usr/bin/env python3
'''The module contains the definition of the "DB" class'''
import requests
from uuid import uuid4

BASE_URL = "http://127.0.0.1:5000"
UUID_LEN = len(str(uuid4()))


def register_user(email: str, password: str) -> None:
    '''Testing "POST /users" to register a new user'''
    url = BASE_URL + "/users/"
    data = {"email": email, "password": password}

    res = requests.post(url, data=data)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}

    res = requests.post(url, data=data)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}

    for data in ({}, {"email": email}, {"password": password}):
        res = requests.post(url, data=data)
        assert res.status_code == 400


def log_in_wrong_password(email: str, password: str) -> None:
    '''Testing "POST /sessions" to login with a wrong password'''
    url = BASE_URL + "/sessions/"
    data = {"email": email, "password": password}

    res = requests.post(url, data=data)
    assert res.status_code == 401
    assert res.cookies.get("session_id") is None

    for data in ({}, {"email": email}, {"password": password}):
        res = requests.post(url, data=data)
        assert res.status_code == 400


def log_in(email: str, password: str) -> str:
    '''Testing "POST /sessions" to login with a valid password'''
    url = BASE_URL + "/sessions/"
    data = {"email": email, "password": password}

    res = requests.post(url, data=data)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    session_id = res.cookies.get("session_id")
    assert session_id is not None
    assert len(session_id) == UUID_LEN

    return session_id


def profile_unlogged() -> None:
    '''Testing "GET /profile/" when the user is not logged in'''
    url = BASE_URL + "/profile/"

    res = requests.get(url)
    assert res.status_code == 403

    res = requests.get(url, cookies={"session_id": "what_is_cookies"})
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    '''Testing "GET /profile/" when the user is logged in'''
    url = BASE_URL + "/profile/"

    res = requests.get(url, cookies={"session_id": session_id})
    assert res.status_code == 200
    assert list(res.json().keys()) == ["email"]


def log_out(session_id: str) -> None:
    '''Testing "DELETE /sessions" to logout'''
    url = BASE_URL + "/sessions/"

    res = requests.delete(url)
    assert res.status_code == 403

    res = requests.delete(url, cookies={"session_id": "Fake_session_id"})
    assert res.status_code == 403

    res = requests.delete(url, cookies={"session_id": session_id},
                          allow_redirects=False)
    assert res.status_code == 302
    assert res.ok
    assert res.is_redirect
    assert res.raw.get_redirect_location() == "/"
    assert res.next.url == BASE_URL + "/"


def reset_password_token(email: str) -> str:
    '''Testing "POST /reset_password" to generate password reset token'''
    url = BASE_URL + "/reset_password/"
    data = {"email": email}

    res = requests.post(url, data=data)
    assert res.status_code == 200
    res_dict = res.json()
    assert sorted(list(res_dict.keys())) == ["email", "reset_token"]
    assert res_dict.get("email") == email
    reset_token = res_dict.get("reset_token")
    assert reset_token is not None
    assert len(reset_token) == UUID_LEN

    for data in ({}, {"email": "du@mm.y"}):
        res = requests.post(url, data=data)
        assert res.status_code == 403

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''Testing "PUT /reset_password" to generate password reset token'''
    url = BASE_URL + "/reset_password/"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
        }

    res = requests.put(url, data=data)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}

    test_payloads = (
        {},
        {"email": "du@mm.y"},
        {"email": "du@mm.y", "reset_token": "dummy_reset_token"},
        {"email": email, "reset_token": reset_token}
    )
    for data in test_payloads:
        res = requests.put(url, data=data)
        assert res.status_code == 403


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
