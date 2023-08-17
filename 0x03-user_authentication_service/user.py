#!/usr/bin/env python3
"""Create a SQL Alchemy models called User"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column


Base = declarative_base()


class User(Base):
    """Create a mapping object to a table called 'users' in the database"""
    __tablename__: str = 'users'
    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: str = Column(String(250))
    reset_token: str = Column(String(250))
