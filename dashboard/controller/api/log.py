from dashboard.core.webapp import WEBAPP
from rasp.utils.log import logger
from dashboard.utils.web import json_data, login_required, get_page_and_size, get_pagination

from dashboard.models.message import Message

from flask import request
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

@WEBAPP.route("/api/log/alarm", methods=["POST"])
@login_required
def get_alarm_log_by_params():
    req_data = request.form.to_dict()
    page, size = get_page_and_size(request.args)
    start, end = get_pagination(page, size)
    msg_obj_list = Message.query.filter_by(**req_data).slice(start, end).all()
    msg_dict_list = [msg_obj.serialize() for msg_obj in msg_obj_list]
    return json_data(msg_dict_list)
