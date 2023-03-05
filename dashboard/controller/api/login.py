from dashboard.core.webapp import WEBAPP
from dashboard.utils.web import json_data
from rasp.core.app import RASP_APP
from rasp.core.script import script_context_manager

from flask import session, request

@WEBAPP.route("/api/register", method=["POST"])
def register():

    return json_data({
        "status": 200
    })

@WEBAPP.route("/api/login", methods=["POST"])
def login():
    
    return json_data({
        "status": 200,
        "data": script_context_manager.get_script_context_dict()
    })