#!/usr/bin/env python3
'''The module contains the definition of the "DB" class'''
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    '''DB management class'''

    def __init__(self) -> None:
        '''Initialize a new DB instance'''
        self._engine = create_engine("sqlite:///a.db", echo=True)
        self._engine.echo = False  # Temporary
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        '''Memoized session object'''
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''Creates a new User instance and inserts it in the db'''
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        '''Updates the "User" object attributes using the input tkeyword
        arguments, then commit the changes to the database'''
        try:
            user = self.find_user_by(id=user_id)
        except (InvalidRequestError, NoResultFound):
            raise ValueError

        for key, val in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, val)

        self._session.commit()

    def find_user_by(self, *args, **kwargs) -> User:
        '''Returns the first row found in a query of `users` table
        filtered by the "kwargs" input arguments'''
        res = self._session.query(User).filter_by(**kwargs)[0:1]

        if not len(res):
            raise NoResultFound
        return res[0]
