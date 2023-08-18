#!/usr/bin/env python3
"""Contain functions to manage authentication"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    pwd_in_bytes: bytes = password.encode('utf-8')
    return bcrypt.hashpw(pwd_in_bytes, bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a unique identifier"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize storage instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user to the database"""
        if type(password) is str and type(email) is str:
            hashed_password: bytes = _hash_password(password)
            try:
                user: User = self._db.find_user_by(email=email)
                raise ValueError('User {} already exists'.format(email))
            except NoResultFound:
                user = self._db.add_user(email, hashed_password)
                return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if a login is valid"""
        if type(email) is str and type(password) is str:
            try:
                user: User = self._db.find_user_by(email=email)
                pwd: bytes = password.encode('utf-8')
                return bcrypt.checkpw(pwd, user.hashed_password)
            except NoResultFound:
                return False

    def create_session(self, email: str) -> str:
        """Create a user session"""
        assert type(email) is str
        try:
            user: User = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get a user from a session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """Destroy a user session"""
        assert type(user_id) is str
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except (ValueError, NoResultFound):
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Create a password reset token"""
        assert type(email) is str
        try:
            user: User = self._db.find_user_by(email=email)
            user.reset_token = _generate_uuid()
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Change a user's password"""
        assert type(reset_token) is str and type(password) is str
        try:
            user: User = self._db.find_user_by(reset_token=reset_token)
            pwd: bytes = password.encode('utf-8')
            hashed_pwd: bytes = bcrypt.hashpw(pwd, bcrypt.gensalt())
            user.hashed_password = hashed_pwd
            return None
        except NoResultFound:
            raise ValueError
