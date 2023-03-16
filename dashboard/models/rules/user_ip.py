from __future__ import annotations

from dashboard.core.db import DB_BASE
from dashboard.core.db import DB_SESSION, WEBAPP
from rasp.core.rule import RuleType, AbstractRule

from sqlalchemy import Column, Integer, String

class UserIPRule(AbstractRule):
    __tablename__ = 'user_ip_ruler'
    filename = __tablename__ + ".json"

    id = Column(Integer, primary_key=True)
    data = Column(String(512))
    rule_type = Column(Integer)

    def __init__(self, 
        data: str = "", 
        rule_type: int = RuleType.BLACKLIST
    ):
        self.data = data
        self.rule_type = rule_type

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'data': self.data,
            'rule_type': self.rule_type
        }
    
    @staticmethod
    def deserialize(data: dict) -> UserIPRule:
        return UserIPRule(data['data'], data['rule_type'])
    
    def import_rules(self):
        with WEBAPP.app_context():
            DB_SESSION.add(self)
            DB_SESSION.commit()
    
    @staticmethod
    def export_rules() -> list:
        with WEBAPP.app_context():
            q_list = DB_SESSION.query(UserIPRule).all()
            return [q.serialize() for q in q_list]

        