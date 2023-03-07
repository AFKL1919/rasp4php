from __future__ import unicode_literals
from rasp.core.filter import AbstractFilter, FilterResult, FilterContext
from dashboard.models.rules.network import NetworkRule
from rasp.core.rule import RULE_MANAGER, RuleType
from builtins import super
from enum import Enum
from ipaddress import ip_address, ip_network
from urllib.parse import urlparse
from typing import List
from future.standard_library import install_aliases
install_aliases()
from rasp.utils.log import logger


class DefaultNetworkFilter(AbstractFilter):

    rule = dict()
    name = 'DefaultNetworkFilter'
    context = FilterContext.URL
    rule_method = NetworkRule

    class rule_entries(Enum):
        WHITELIST_DOMAIN = 0
        WHITELIST_IP = 1
        BLACKLIST_DOMAIN = 2
        BLACKLIST_IP = 3

    def __init__(self):
        super().__init__()
        RULE_MANAGER.init_rule_manager(self.rule_method, self.name)
        rule_list = RULE_MANAGER.get_rule_list(self.name)

        self.rule[self.rule_entries.WHITELIST_DOMAIN] = list()
        self.rule[self.rule_entries.WHITELIST_IP] = list()
        self.rule[self.rule_entries.BLACKLIST_DOMAIN] = list()
        self.rule[self.rule_entries.BLACKLIST_IP] = list()
        self.init_filter_rule(rule_list)

    def init_filter_rule(self, rule_list: List[NetworkRule]):
        for rule in rule_list:
            rule_m = self.rule_method(rule)
            self._init_filter_rule(rule_m)

    def _init_filter_rule(self, rule: NetworkRule):
        if rule.rule_type == RuleType.BLACKLIST:
            if rule.is_domain():
                self.rule[self.rule_entries.BLACKLIST_DOMAIN].append(rule)
            else:
                self.rule[self.rule_entries.BLACKLIST_IP].append(rule)
        elif rule.rule_type == RuleType.WHITELIST:
            if rule.is_domain():
                self.rule[self.rule_entries.WHITELIST_DOMAIN].append(rule)
            else:
                self.rule[self.rule_entries.WHITELIST_IP].append(rule)

    def is_unix_domain(self, url):
        return urlparse(url).scheme == 'unix'

    def has_suspicious_scheme(self, url):
        return urlparse(url).scheme not in (
            '',
            'http',
            'https',
            'ftp',
            'ftps',
            'ssh2.shell',
            'ssh2.exec',
            'ssh2.tunnel',
            'ssh2.sftp',
            'ssh2.scp',
        )

    def get_unobfuscated_ip(self, netloc):
        try:
            # 尝试直接解析IP地址
            return str(ip_address(netloc))
        except ValueError:
            pass

        try:
            # 尝试将16进制的IP地址转换为整数后解析
            return str(ip_address(int(netloc, 0)))
        except ValueError:
            pass

        try:
            # 尝试将类似 0x7f.0x0.0x0.0x1 格式的IP地址转换为字符串再解析
            if '.' in netloc:
                parts = netloc.split('.')
                if len(parts) == 4:
                    ip = '.'.join([str(int(p, 0)) for p in parts])
                    return str(ip_address(ip))
        except Exception:
            pass

        # 所有尝试失败，返回 None
        return None

    def _get_rule(self, rule_entries: rule_entries) -> List[NetworkRule]:
        if self.rule[rule_entries]:
            return self.rule[rule_entries]
        else:
            return list()

    def is_whitelisted_domain(self, netloc):
        whilelist_domain = self._get_rule(self.rule_entries.WHITELIST_DOMAIN)
        return whilelist_domain and any(d.data in netloc for d in whilelist_domain)

    def is_whitelisted_ip(self, netloc):
        whilelist_ip = self._get_rule(self.rule_entries.WHITELIST_IP)
        return whilelist_ip and any(d.data in netloc for d in whilelist_ip)

    def is_blacklisted_domain(self, netloc):
        blacklist_domain = self._get_rule(self.rule_entries.BLACKLIST_DOMAIN)
        return blacklist_domain and any(d.data in netloc for d in blacklist_domain)

    def is_blacklisted_ip(self, netloc):
        blacklist_ip = self._get_rule(self.rule_entries.BLACKLIST_IP)
        return blacklist_ip and any(d.data in netloc for d in blacklist_ip)

    def filter(self, message):
        for url in message['normalized_args']:
            u = urlparse(url)

            if self.is_unix_domain(u):
                return FilterResult.IGNORE

            if self.has_suspicious_scheme(u):
                return FilterResult.ALERT

            host = u.netloc
            ip = self.get_unobfuscated_ip(host)

            if ip is not None:
                if self.is_whitelisted_ip(ip):
                    return FilterResult.IGNORE
                if self.is_blacklisted_ip(ip):
                    return FilterResult.ALERT
            else:
                # domain
                if self.is_whitelisted_domain(host):
                    return FilterResult.IGNORE
                if self.is_blacklisted_domain(host):
                    return FilterResult.ALERT

        return FilterResult.DEFAULT
