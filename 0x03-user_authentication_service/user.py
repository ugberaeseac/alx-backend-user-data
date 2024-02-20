#!/usr/bin/env python3
"""
SQLalchemy user model with attributes
    id: integer primary key
    email: a non-nullable string
    hashed_password: a non-nullable string
    session_id: a nullable string
    reset_token: a nullable string
"""

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """
    SQLalchemy model User for a database table
    users
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_passord = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
