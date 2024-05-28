#!/usr/bin/env python3
'''The module contains the definition of the "Auth" class'''
from typing import Optional
from uuid import uuid4

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    '''Returns salted hash the string "password"'''
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    '''Returns string representation of a new UUID'''
    return str(uuid4())


class Auth:
    '''Auth: class to handle the interaction with the authentication database
    '''

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''Registers a new user with "email" and "password" in the DB using'''
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed = _hash_password(password).decode("utf-8")
            return self._db.add_user(email, hashed)

    def valid_login(self, email: str, password: str) -> bool:
        '''Checks if login credentials are valid or not'''
        try:
            user = self._db.find_user_by(email=email)
            hashed = user.hashed_password.encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), hashed):
                return True
            return False

        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        '''Creates a session for the "User" with email "email" and returns
        the session ID'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        '''Return the corresponding "User" instance, to the session with
        "session_id" if found or None elsewise'''
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        '''Destroy the session for the "User" instance with id = <user_id>"'''
        if user_id is None:
            return None

        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        '''Generates a UUID and update the "User" object attribute
        "reset_token", if the user exists and returns the generated token'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = str(uuid4)
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        '''Updates the "User" object attribute "password" and resets
        "reset_token" to None'''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed = _hash_password(password).decode("utf-8")
        self._db.update_user(user.id,
                             hashed_password=hashed, reset_token=None)
        return None
