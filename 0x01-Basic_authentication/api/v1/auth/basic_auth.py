#!/usr/bin/env python3
"""
Basic Authentication API
    inherits from Auth class
"""


from api.v1.auth.auth import Auth


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
