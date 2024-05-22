#!/usr/bin/env python3
'''Session Athentication Module'''
from typing import TypeVar
from uuid import uuid4

from api.v1.auth.auth import Auth
from models.user import User


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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''Returns a User ID based on a Session ID'''
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''Returns a <User> instance based on a cookie value'''
        if request is None:
            return None

        user_id = self.user_id_for_session_id(self.session_cookie(request))
        if user_id is None:
            return None

        user_search_results = User.search({"id": user_id})

        if not len(user_search_results):
            return None
        return user_search_results[0]

    def destroy_session(self, request=None):
        '''Deletes the user session'''
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
