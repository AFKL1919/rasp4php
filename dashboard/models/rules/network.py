from __future__ import annotations

from dashboard.core.db import DB_BASE
from dashboard.core.db import DB_SESSION, WEBAPP
from rasp.core.rule import RuleType, AbstractRule

from sqlalchemy import Column, Integer, String

class NetworkRule(AbstractRule):
    __tablename__ = 'network_ruler'
    filename = __tablename__ + ".json"

    id = Column(Integer, primary_key=True)
    data = Column(String(512))
    data_type = Column(String(32))
    rule_type = Column(Integer)

    def __init__(self, 
        data: str = "", 
        data_type: str = "", 
        rule_type: int = RuleType.BLACKLIST
    ):
        self.data = data
        self.data_type = data_type
        self.rule_type = rule_type

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'data': self.data,
            'data_type': self.data_type,
            'rule_type': self.rule_type
        }
    
    def is_domain(self) -> bool:
        return self.data_type == "domain"
    
    def is_ip(self) -> bool:
        return self.data_type == "ip"
    
    @staticmethod
    def deserialize(data: dict) -> NetworkRule:
        return NetworkRule(data['data'], data['data_type'], data['rule_type'])
    
    def import_rules(self):
        with WEBAPP.app_context():
            DB_SESSION.add(self)
            DB_SESSION.commit()
    
    @staticmethod
    def export_rules() -> list:
        with WEBAPP.app_context():
            q_list = DB_SESSION.query(NetworkRule).all()
            return [q for q in q_list]

        