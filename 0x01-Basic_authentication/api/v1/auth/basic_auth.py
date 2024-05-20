#!/usr/bin/env python3
'''Basic Athentication Module'''
from base64 import b64decode
import binascii

from .auth import Auth


class BasicAuth(Auth):
    '''Basic Athentication class'''

    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        '''Returns the Base64 part of the Authorization header for a Basic
        Authentication'''
        if (
          authorization_header is None or
          type(authorization_header) != str or
          authorization_header[:6] != "Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
      ) -> str:
        '''Returns the decoded value of a Base64 string
        "base64_authorization_header"'''
        b64ah = base64_authorization_header
        if b64ah is None or type(b64ah) != str:
            return None
        try:
            return b64decode(base64_authorization_header).decode("utf-8")
        except binascii.Error:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        '''Returns the user email and password from the Base64 decoded value
        '''
        val = decoded_base64_authorization_header
        if val is None or type(val) != str or val.find(':') < 0:
            return None, None
        return tuple(val.split(":", 1))
