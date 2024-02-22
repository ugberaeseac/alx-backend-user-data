#!/usr/bin/env python3
"""
Encrypting password
returns a salted hashed password in byte string
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    hash the password
    """
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    check if password is valid
    returns true if valid else false
    """
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    return False
