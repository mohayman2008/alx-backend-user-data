#!/usr/bin/env python3
'''Session with Expiration and Persistence Athentication Module'''
from datetime import datetime, timedelta

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth (SessionExpAuth):
    '''Session with Expiration and Persistence Athentication class'''

    def create_session(self, user_id: str = None) -> str:
        '''Creates a Session for a "user_id", saves it to db
        and returns the Session ID'''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        init_dict = {"user_id": user_id, "session_id": session_id}
        UserSession(**init_dict).save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''Returns a User ID based on a Session ID'''
        if session_id is None:  # or type(session_id) != str:
            return None

        session = UserSession.search({"session_id": session_id})
        # try:
        #     session = UserSession.search({"session_id": session_id})
        # except KeyError:
        #     return None

        if len(session) == 0:
            return None
        session = session[0]

        if self.session_duration <= 0:
            return session.user_id

        session_duration = timedelta(seconds=self.session_duration)
        if session.created_at + session_duration < datetime.now():
            # session.remove()
            return None
        return session.user_id

    def destroy_session(self, request=None):
        '''Deletes the user session'''
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        session = UserSession.search({"id": session_id})
        if len(session) == 0:
            return None
        session[0].remove()
        return True
