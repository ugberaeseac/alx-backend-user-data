#!/usr/bin/env python3
"""
Encrypting password
returns a salted hashed password in byte string
"""


import bcrypt


salt = bcrypt.gensalt()


def hash_password(password: str) -> bytes:
    """
    hash the password
    """
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd
