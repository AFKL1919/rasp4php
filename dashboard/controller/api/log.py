from dashboard.core.webapp import WEBAPP
from dashboard.utils.web import json_data
from rasp.utils.log import logger

from dashboard.models.message import Message

from json import loads as json_loads

@WEBAPP.route("/api/log/install", methods=["GET"])
def get_install_log():
    return 233

@WEBAPP.route("/api/log/alarm", methods=["GET"])
def get_alarm_log():
    msg_dict_list = list()
    msg_obj_list = Message.query.all()
    for msg_obj in msg_obj_list:
        msg_obj_dict = dict(msg_obj.__dict__)
        
        msg_obj_dict.pop('_sa_instance_state')
        msg_obj_dict['args'] = json_loads(msg_obj_dict['args'])
        msg_obj_dict['normalized_args'] = json_loads(msg_obj_dict['normalized_args'])

        msg_dict_list.append(msg_obj_dict)
        
    return json_data(msg_dict_list)
