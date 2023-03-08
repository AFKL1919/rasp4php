from __future__ import unicode_literals
from typing import List
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from builtins import super

from rasp.utils.log import logger
from rasp.core.rule import RULE_MANAGER, RuleType
from dashboard.models.rules.script import ScriptRule
from rasp.core.filter import AbstractFilter, FilterResult, FilterContext


class DefaultScriptFilter(AbstractFilter):

    rule = dict()
    name = 'DefaultScriptFileFilter'
    context = FilterContext.ANY
    rule_method = ScriptRule

    def __init__(self):
        super().__init__()
        RULE_MANAGER.init_rule_manager(self.rule_method, self.name)
        rule_list = RULE_MANAGER.get_rule_list(self.name)

        self.rule[RuleType.BLACKLIST] = list()
        self.rule[RuleType.WHITELIST] = list()
        self.init_filter_rule(rule_list)

    def init_filter_rule(self, rule_list: List[ScriptRule]):
        for rule in rule_list:
            if rule.rule_type == RuleType.BLACKLIST:
                self.rule[RuleType.BLACKLIST].append(rule)
            elif rule.rule_type == RuleType.WHITELIST:
                self.rule[RuleType.WHITELIST].append(rule)

    def _is_whitelisted(self, whitelisted_file: Path, filename: str) -> bool:
        return whitelisted_file == filename or whitelisted_file.is_dir() and whitelisted_file in Path(filename).parents

    def is_whitelisted(self, filename):
        if not self.rule[RuleType.WHITELIST]:
            return False

        whitelist = [Path(script_ruler.data)
                     for script_ruler in self.rule[RuleType.WHITELIST]]
        return any(self._is_whitelisted(whitelisted_file, filename) for whitelisted_file in whitelist)

    def filter(self, message):
        if 'filename' not in message or 'lineno' not in message:
            return FilterResult.DEFAULT

        suspicious_file = ":".join(
            (message['filename'], str(message['lineno'])))

        if self.is_whitelisted(suspicious_file):
            return FilterResult.IGNORE

        return FilterResult.DEFAULT
