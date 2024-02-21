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


def _hash_password(password: str) -> bytes:
    """
    hash the password
    """
    if password:
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_pwd
