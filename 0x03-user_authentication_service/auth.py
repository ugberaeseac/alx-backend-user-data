#!/usr/bin/env python3
"""
_hash_password method
takes a password string as arguments and returns
a salted hash of the input password in bytes
"""


from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from uuid import uuid4
salt = bcrypt.gensalt()


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register a new user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)
            return new_user
        else:
            msg = "User {} already exists"
            raise ValueError(msg.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        validate the email and password
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        generate a new UUID and store it in the
        database's user session_id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        return the corresponding User using the session_id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user

        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroy a session
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None
        return None

    def get_reset_password_token(email: str) -> str:
        """
        Generate a reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError


def _hash_password(password: str) -> bytes:
    """
    hash the password
    """
    if password:
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_pwd


def _generate_uuid() -> str:
    """
    return a string representation of a new UUID
    """
    return (str(uuid4()))
