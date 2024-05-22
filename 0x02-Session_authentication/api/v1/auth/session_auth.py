#!/usr/bin/env python3
'''Session Athentication Module'''
from typing import TypeVar
from uuid import uuid4

from api.v1.auth.auth import Auth
# from models.user import User


class SessionAuth(Auth):
    '''Session Athentication class'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''Creates a Session for a "user_id" and returns the Session ID'''
        if user_id is None or type(user_id) != str:
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id
