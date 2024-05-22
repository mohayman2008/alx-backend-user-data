#!/usr/bin/env python3
'''Session with Expiration Athentication Module'''
from datetime import datetime, timedelta
from os import getenv

from api.v1.auth.session_auth import SessionAuth
# from models.user import User

SESSION_DURATION = getenv("SESSION_DURATION", 0)
try:
    SESSION_DURATION = int(SESSION_DURATION)
except Exception:
    SESSION_DURATION = 0


class SessionExpAuth (SessionAuth):
    '''Session with Expiration Athentication class'''

    def __init__(self):
        self.session_duration = SESSION_DURATION

    def create_session(self, user_id: str = None) -> str:
        '''Creates a Session for a "user_id" and returns the Session ID'''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''Returns a User ID based on a Session ID'''
        if session_id is None or type(session_id) != str:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        session_duration = timedelta(seconds=self.session_duration)
        if created_at is None or\
                created_at + session_duration < datetime.now():
            return None
        return session_dict.get("user_id")
