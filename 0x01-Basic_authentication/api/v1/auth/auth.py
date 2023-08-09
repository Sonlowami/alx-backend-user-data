#!/usr/bin/env python3
"""Contain an authorization class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Contain methods and properties used for authorizing a user"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Find if a path requires authorization or not"""
        if not path or not excluded_paths:
            return True
        if path[-1] != '/':
            s_path = path + '/'
        else:
            s_path = path[:-1]
        if path not in excluded_paths and s_path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Return the value in the authorization header"""
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None"""
        return None
