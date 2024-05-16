#!/usr/bin/env python3
'''The module contain functions to hash and '''
import bcrypt  # type: ignore


def hash_password(password: str) -> bytes:
    '''The function generates and returns a salted, hashed bytes string
    password from the input string "password"'''
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''The function validate that the provided "password" matches
    "hashed_password"'''
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
