from __future__ import unicode_literals
from rasp.core.filter import AbstractFilter, FilterResult, FilterContext
from rasp.core.rule import RULE_MANAGER, RuleType
from dashboard.models.rules.file import FileRule
from builtins import super
from urllib.parse import urlparse
from typing import List
from future.standard_library import install_aliases
install_aliases()


class DefaultFileFilter(AbstractFilter):

    rule = dict()
    name = 'DefaultFileFilter'
    context = FilterContext.FILE
    rule_method = FileRule

    def __init__(self):
        super().__init__()
        RULE_MANAGER.init_rule_manager(self.rule_method, self.name)
        rule_list = RULE_MANAGER.get_rule_list(self.name)

        self.rule[RuleType.BLACKLIST] = list()
        self.rule[RuleType.WHITELIST] = list()
        self.init_filter_rule(rule_list)

    def init_filter_rule(self, rule_list: List[FileRule]):
        for rule in rule_list:
            if rule.rule_type == RuleType.BLACKLIST:
                self.rule[RuleType.BLACKLIST].append(rule)
            elif rule.rule_type == RuleType.WHITELIST:
                self.rule[RuleType.WHITELIST].append(rule)

    def is_whitelisted(self, filename: str) -> bool:
        return any(f.data in filename for f in self.rule[RuleType.WHITELIST])

    def is_blacklisted(self, filename):
        return any(f.data in filename for f in self.rule[RuleType.BLACKLIST])

    def has_suspicious_scheme(self, filename):
        urlparsed_result = urlparse(filename)
        return urlparsed_result.scheme in ('data', 'php', 'expect')

    def has_file_scheme(self, filename):
        urlparsed_result = urlparse(filename)
        return urlparsed_result.scheme in ('', 'file')

    def filter(self, message):
        for file_accessed in message['args']:
            if self.has_suspicious_scheme(file_accessed):
                return FilterResult.ALERT

            if not self.has_file_scheme(file_accessed):
                return FilterResult.IGNORE

            for normalized_filename in message['normalized_args']:
                if self.is_blacklisted(normalized_filename):
                    return FilterResult.ALERT

                if self.is_whitelisted(normalized_filename):
                    return FilterResult.IGNORE

        return FilterResult.DEFAULT
