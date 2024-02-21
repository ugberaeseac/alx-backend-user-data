#!/usr/bin/env python3
"""
_hash_password method
takes a password string as arguments and returns
a salted hash of the input password in bytes
"""


import bcrypt
salt = bcrypt.gensalt()


def _hash_password(password: str) -> bytes:
    """
    hash the password
    """
    if password:
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_pwd
