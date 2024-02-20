#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        add a user to the database
        returns a User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        query the database with arbituary keyword arguments
        return the first row found in the users table
        """
        if kwargs is None:
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if user:
            return user
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        update a user attribute
        returns None
        """
        if type(user_id) is not int:
            raise ValueError

        if user_id is None or kwargs is None:
            raise InvalidRequestError

        user = self.find_user_by(id=user_id)
        if not user:
            raise NoResultFound

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
