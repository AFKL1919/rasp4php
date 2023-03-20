from dashboard.core.webapp import WEBAPP
from rasp.utils.log import logger
from dashboard.utils.web import json_data, login_required

from dashboard.models.message import Message

from json import loads as json_loads

@WEBAPP.route("/api/log/install", methods=["GET"])
def get_install_log():
    return 233

@WEBAPP.route("/api/log/alarm", methods=["GET"])
@login_required
def get_alarm_log():
    msg_obj_list = Message.query.all()
    msg_dict_list = [msg_obj.serialize() for msg_obj in msg_obj_list]
    
    return json_data(msg_dict_list)
