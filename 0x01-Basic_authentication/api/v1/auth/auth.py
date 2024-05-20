#!/usr/bin/env python3
'''Athentication Module'''
from typing import List, TypeVar

from flask import request


class Auth:
    '''Athentication abstract base class'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Checks if a path requires authentication or not'''
        if None in (path, excluded_paths) or not len(excluded_paths):
            return True
        path += '/' if path[-1] != '/' else ''
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        '''Returns the value of the request header "Authorization"'''
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        ''''''
        return None
