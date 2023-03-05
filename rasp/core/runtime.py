from __future__ import unicode_literals
from os import geteuid, uname
from builtins import super

from rasp.utils.log import logger

def check_permission(uid):
    if uid != 0:
        return False
    return True

class Runtime(object):
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.environment = {}
        self.environment['euid'] = geteuid()
        self.environment['platform'] = uname()[0]
