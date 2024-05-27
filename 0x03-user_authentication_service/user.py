#!/usr/bin/env python3
'''The module contains the "Base" class generated by the SQLAlchemy
declarative_base class maker and the definition of the DB mapped class "User"
'''
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    '''User: DB model for table "users"'''

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
