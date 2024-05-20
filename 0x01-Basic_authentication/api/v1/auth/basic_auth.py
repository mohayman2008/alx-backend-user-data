#!/usr/bin/env python3
'''Basic Athentication Module'''
from .auth import Auth


class BasicAuth(Auth):
    '''Basic Athentication class'''

    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        '''Returns the Base64 part of the Authorization header for a Basic
        Authentication'''
        if (
          not authorization_header or
          type(authorization_header) != str or
          authorization_header[:6] != "Basic "):
            return None
        return authorization_header[6:]
