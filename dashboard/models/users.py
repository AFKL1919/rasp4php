from dashboard.core.webapp import WEBAPP
from dashboard.core.db import DB_BASE, DB_SESSION

from hashlib import sha1
from sqlalchemy import Column, Integer, String


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
        self.password = Users.hash_user_password(password)
    
    @staticmethod
    def hash_user_password(password: str) -> str:
        return sha1(password.encode()).hexdigest()
    
    def serialize(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'permission': self.permission
        }
    
    @staticmethod
    def register(username: str, password: str, permission: int = 1) -> 'Users':
        if Users.query.filter(Users.username == username).first() != None:
            return None
        
        return Users(username, password, permission)