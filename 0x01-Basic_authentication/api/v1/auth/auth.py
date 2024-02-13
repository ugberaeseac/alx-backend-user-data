#!/usr/bin/python3
"""
Manage API authentication
    create Auth class
    class is the template for all authentication system you will implement.
"""


from flask import request
from typing import List, TypeVar


class Auth():
    """
    Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        requires authentication
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'

        if excluded_paths[-1] != '/':
            excluded_paths += '/'

        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """
        authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user
        """
        return None
