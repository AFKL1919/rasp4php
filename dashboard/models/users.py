from dashboard.core.db import DB_BASE

from hashlib import sha1
from sqlalchemy import Column, Integer, String, DATETIME


class Users(DB_BASE.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(120))
    password = Column(String(120))

    ADMIN_USER = 0
    NORMAL_USER = 1
    permission = Column(Integer)

    def __init__(self, username: str, password: str, permission: int = 1):
        self.permission = permission
        self.username = username
        self.password = self.user_password_hash(password)
    
    def user_password_hash(password: str):
        return sha1(password.encode()).hexdigest()