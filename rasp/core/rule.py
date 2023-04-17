from __future__ import unicode_literals, annotations
import json
from enum import Enum
from typing import List
from abc import abstractmethod

from rasp.utils.log import logger
from dashboard.core.db import DB_BASE
from rasp.common.config import DEFAULT_RULE_DIR, Path


class RuleType(Enum):
    """Rule type enumeration."""

    WHITELIST = 0
    BLACKLIST = 1

class AbstractRule(DB_BASE.Model):

    filename = "rule.json"
    __abstract__ = True

    def __init__(self):
        pass

    @abstractmethod
    def serialize(self) -> dict:
        return dict()
    
    @staticmethod
    @abstractmethod
    def deserialize(data: dict) -> AbstractRule:
        pass
    
    @abstractmethod
    def import_rules(self):
        pass

    @staticmethod
    @abstractmethod
    def export_rules() -> List[AbstractRule]:
        return list()


class RuleManager(object):
    """Managing rules"""

    rules = dict()

    def __init__(self):
        logger.info("Rule Manager init.")

    def import_rules_to_database(self, data, rule_method: AbstractRule) -> list:
        rule_obj_list = list()

        for rule in data:
            rule_obj = rule_method.deserialize(rule)
            rule_obj.import_rules()
            rule_obj_list.append(rule_obj)
        
        return rule_obj_list
        
    def init_rule_manager(self, rule_method: AbstractRule, filter_class_name: str) -> list:
        file = DEFAULT_RULE_DIR / Path(rule_method.filename)
        if file.exists():
            rule_data_list = json.loads(file.read_text(encoding='utf-8'))
            rule_obj_list = self.import_rules_to_database(rule_data_list, rule_method)
        else:
            rule_obj_list = list()
        
        self.rules[filter_class_name] = rule_obj_list
    
    def update_rule(self, rule_method: AbstractRule, filter_class_name: str):
        rule_list = rule_method.export_rules()
        self.rules[filter_class_name] = rule_list
            
    def get_rule_list(self, filter_class_name: str) -> list:
        if filter_class_name not in self.rules:
            return list()
        return self.rules[filter_class_name]
    
    def get_all_rules(self) -> dict:
        return self.rules

    def dump_rules_to_file(self, filter_class_name: str):
        rules = self.rules[filter_class_name]

        if not rules:
            return

        path = Path(rules[0].filename)
        path.write_text(
            json.dumps([rule.serialize() for rule in rules]), encoding='utf-8'
        )

        return path


RULE_MANAGER = RuleManager()