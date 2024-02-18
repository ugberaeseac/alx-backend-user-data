#!/usr/bin/env python3
"""
Manage API authentication
    create Auth class
    class is the template for all authentication system you will implement.
"""


from flask import request
from typing import List, TypeVar
from os import getenv


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

        for excluded in excluded_paths:
            if excluded.endswith('*'):
                prefix = excluded[:-1]
                if path.startswith(prefix):
                    return False

        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """
        authorization header
        """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user
        """
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
