#!/usr/bin/env python3
'''The module contains the definition of the "Auth" class'''
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
