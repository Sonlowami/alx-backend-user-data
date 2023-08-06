#!/usr/bin/env python3
"""This module contain functions that encrypts user information before
storing in the database"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Generate a hash of a function"""
    password = bytes(password, encoding='utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a password is correct"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
