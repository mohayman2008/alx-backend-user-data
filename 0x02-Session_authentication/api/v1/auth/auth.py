#!/usr/bin/env python3
'''Athentication Module'''
from os import getenv
from re import match
from typing import List, TypeVar

from flask import request

SESSION_NAME = getenv("SESSION_NAME", "_my_session_id")


class Auth:
    '''Athentication abstract base class'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Checks if a path requires authentication or not'''
        if None in (path, excluded_paths) or not len(excluded_paths):
            return True

        path += '/' if path[-1] != '/' else ''
        if any(map(lambda x: match(rf"^{x.replace('*', '.*?')}", path),
                   excluded_paths)):
            return False
        return True

    def authorization_header(self, request=None) -> str:
        '''Returns the value of the request header "Authorization"'''
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        '''Dummy DocString'''
        return None

    def session_cookie(self, request=None):
        '''Returns the Session ID cookie value from a request'''
        if request is None:
            return None
        return request.cookies.get(SESSION_NAME)
