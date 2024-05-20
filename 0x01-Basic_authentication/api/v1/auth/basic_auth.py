#!/usr/bin/env python3
'''Basic Athentication Module'''
from base64 import b64decode
import binascii
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


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
            decoded = b64decode(base64_authorization_header.encode("utf-8"))
            return decoded.decode("utf-8")
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

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        '''Returns the User instance based on email and password'''
        email_pwd = [user_email, user_pwd]
        if None in email_pwd or any(map(lambda x: type(x) != str, email_pwd)):
            return None
        user_search_results = User.search({"email": user_email})
        if not len(user_search_results):
            return None
        user = user_search_results[0]

        return user if user.is_valid_password(user_pwd) else None

    def current_user(self, request=None) -> TypeVar('User'):
        '''Retrieves the "User" instance for a request'''
        auth_header = self.authorization_header(request)
        b64 = self.extract_base64_authorization_header(auth_header)
        auth_decoded = self.decode_base64_authorization_header(b64)
        email, pwd = self.extract_user_credentials(auth_decoded)
        return self.user_object_from_credentials(email, pwd)
