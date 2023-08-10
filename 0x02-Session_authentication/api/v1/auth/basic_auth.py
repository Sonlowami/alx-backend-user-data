#!/usr/bin/env python3
"""Contain a class Basic_Auth"""
from .auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Impliment a basic authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract the base64 part in the authorization header given"""
        if type(authorization_header) != str:
            return None
        elif not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Decode a base64 authorization header"""
        if type(base64_authorization_header) != str:
            return None
        try:
            bytes_obj: bytes = base64.b64decode(base64_authorization_header)
            return bytes_obj.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
                                 self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Get user credentials from decoded value"""
        decoded: str = decoded_base64_authorization_header
        if type(decoded) != str:
            return None, None
        if ':' not in decoded:
            return None, None
        credentials = decoded.split(':')
        return (credentials[0], credentials[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returns an instance of a user with specified email and password"""
        if user_email is None or user_pwd is None:
            return None
        try:
            user = User.search({'email': user_email})[0]
            if user.is_valid_password(user_pwd):
                return user
        except IndexError:
            return None
        except AttributeError:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return a user object from credentials passed in the Authorization
        header of the request"""
        auth_header: str = self.authorization_header(request)
        base64cred: str = self.extract_base64_authorization_header(auth_header)
        str_creds: str = self.decode_base64_authorization_header(base64cred)
        credentials: str = self.extract_user_credentials(str_creds)
        if credentials is None or len(credentials) != 2:
            return None
        user: str = self.user_object_from_credentials(credentials[0],
                                                      credentials[1])
        return user
