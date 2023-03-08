from __future__ import unicode_literals, annotations
import json
from enum import Enum
from typing import List
from abc import abstractmethod

from rasp.utils.log import logger
from dashboard.core.db import DB_BASE
from rasp.common.config import RASP_APP_RESOURCES, Path


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
    DEFAULT_RULE_DIR = RASP_APP_RESOURCES / "rules"

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
        file = self.DEFAULT_RULE_DIR / Path(rule_method.filename)
        if file.exists():
            rule_data_list = json.loads(file.read_text(encoding='utf-8'))
            rule_obj_list = self.import_rules_to_database(rule_data_list, rule_method)
            self.rules[filter_class_name] = rule_obj_list
        else:
            raise FileNotFoundError("Rule file '{}' not found.".format(file))
    
    def update_rule(self, rule_method: AbstractRule, filter_class_name: str):
        rule_list = rule_method.export_rules()
        self.rules[filter_class_name] = rule_list
            
    def get_rule_list(self, filter_class_name: str) -> dict:
        return self.rules[filter_class_name]

    def dump_rule_to_file(self, rule: AbstractRule):
        path = Path(rule.filename)
        path.write_text(json.dumps(rule.serialize()), encoding='utf-8')


RULE_MANAGER = RuleManager()