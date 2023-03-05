from frida.core import Script
from typing import Dict
from threading import Lock

from rasp.utils.message import message_queue
from rasp.core.filter import FilterManager

from dashboard.core.webapp import WEBAPP
from dashboard.models.message import Message
from dashboard.core.db import DB_SESSION

script_context_dict_lock = Lock()

class ScriptContextManager():

    def __init__(self) -> None:

        """
        script_context_dict = {
            "PID": /* pid */,
            "hook_point": /* hook_point */
        }
        """
        self.script_context_dict = dict()
        self.filter_manager = FilterManager()

    def get_script_context_dict(self) -> Dict[str, Script]:
        while True:
            if not script_context_dict_lock.locked():
                _list = list()
                
                for pid in self.script_context_dict:
                    _map = dict()
                    _map["pid"] = pid
                    _map["hook_point"] = list()

                    for hook_point in self.script_context_dict[pid]:
                        _map["hook_point"].append(hook_point)
                    
                    _list.append(_map)
                
                return _list
    
    def remove_script_context_with_pid(self, pid):
        while True:
            if not script_context_dict_lock.locked():
                script_context_dict_lock.acquire()
                if pid in self.script_context_dict:
                    del self.script_context_dict[pid]
                script_context_dict_lock.release()
                return

    def add_script_context(self, pid, hook_point: str, script_context: Script):
        while True:
            if not script_context_dict_lock.locked():
                script_context_dict_lock.acquire()
                if pid not in self.script_context_dict:
                    self.script_context_dict[pid] = dict()
                
                self.script_context_dict[pid][hook_point] = script_context
                script_context_dict_lock.release()
                return
    
    def find_script_context(self, pid, hook_point: str) -> Script:
        while True:
            if not script_context_dict_lock.locked():
                return self.script_context_dict[pid][hook_point]
    
    def script_message_callback(self, message, data):
        # logger.info(message)
        if message['type'] == 'error':
            message_queue.put(message)
            return

        if isinstance(message['payload'], str):
            message_queue.put(message)
            return

        if 'pid' in message['payload']:
            pid = message['payload']['pid']
            hook_point = message['payload']['hook_point']
            script_context = self.find_script_context(pid, hook_point)

            if self.filter_manager.filter(message['payload']):
                message["banned"] = True
                message_queue.put(message)
                script_context.post({
                    "is_blocked": True,
                    "code": 403,
                    "body": "<h1>您的请求存在危险行为</h1>",
                    "headers": {
                        "fuck": "you"
                    }
                })

                with WEBAPP.app_context():
                    DB_SESSION.add(
                        Message(message['payload'])
                    )
                    DB_SESSION.commit()

            else:
                script_context.post({"is_blocked": False})
            return
        
        message_queue.put(message)


script_context_manager = ScriptContextManager()