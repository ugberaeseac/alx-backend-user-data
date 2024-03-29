#!/usr/bin/env python3
"""
Basic Authentication API
    inherits from Auth class
"""


from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Basic Authentication
    inherits from Auth class
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        returns Base64 section of the authorization header
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if authorization_header[:6] != "Basic ":
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        returns decoded value of a
        base64 encoded string
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            encoded = base64.b64decode(base64_authorization_header)
            decoded = encoded.decode('utf-8')
        except BaseException:
            return None

        return decoded

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> str:
        """
        returns the user email and password from
        the Base64 decoded value
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        credentials = decoded_base64_authorization_header.split(':', 1)
        email = credentials[0]
        password = credentials[1]

        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on email and password
        """
        if user_email is None or type(user_email) is not str:
            return None

        if user_pwd is None or type(user_pwd) is not str:
            return None

        try:
            users = User.search({'email': user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        if auth_header:
            encoded_str = self.extract_base64_authorization_header(auth_header)
            if encoded_str:
                decoded_str = self.decode_base64_authorization_header(
                        encoded_str)
                if decoded_str:
                    email, password = self.extract_user_credentials(
                            decoded_str)
                    if email and password:
                        user = self.user_object_from_credentials(
                                email, password)
                        if user:
                            return user
        return None
