from __future__ import unicode_literals
from rasp.core.filter import AbstractFilter, FilterResult, FilterContext
from rasp.core.rule import RULE_MANAGER, RuleType
from rasp.utils.log import logger
from dashboard.models.rules.user_ip import UserIPRule
from builtins import super
from typing import List
from future.standard_library import install_aliases
install_aliases()


class DefaultUserIPFilter(AbstractFilter):

    rule = dict()
    name = 'DefaultUserIPFilter'
    context = FilterContext.START_REQUEST
    rule_method = UserIPRule

    def __init__(self):
        super().__init__()
        RULE_MANAGER.init_rule_manager(self.rule_method, self.name)
        rule_list = RULE_MANAGER.get_rule_list(self.name)

        self.clear_filter_rule()
        self.init_filter_rule(rule_list)
    
    def clear_filter_rule(self):
        self.rule[RuleType.BLACKLIST] = list()
        self.rule[RuleType.WHITELIST] = list()

    def init_filter_rule(self, rule_list: List[UserIPRule]):
        for rule in rule_list:
            rule_type = RuleType(rule.rule_type)
            if rule_type == RuleType.BLACKLIST:
                self.rule[RuleType.BLACKLIST].append(rule)
            elif rule_type == RuleType.WHITELIST:
                self.rule[RuleType.WHITELIST].append(rule)

    def is_whitelisted(self, remote_addr: str) -> bool:
        return any(f.data == remote_addr for f in self.rule[RuleType.WHITELIST])

    def is_blacklisted(self, remote_addr) -> bool:
        return any(f.data == remote_addr for f in self.rule[RuleType.BLACKLIST])

    def filter(self, message):
        remote_addr = message["remote_addr"]
        
        if self.is_blacklisted(remote_addr):
            return FilterResult.ALERT

        if self.is_whitelisted(remote_addr):
            return FilterResult.PASS

        return FilterResult.SAFE
