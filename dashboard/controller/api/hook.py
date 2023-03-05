from dashboard.core.webapp import WEBAPP
from dashboard.utils.web import json_data
from rasp.core.app import RASP_APP
from rasp.core.script import script_context_manager

@WEBAPP.route("/api/hook", methods=["GET"])
def list_hook_point():
    return json_data({
        "status": 200,
        "data": script_context_manager.get_script_context_dict()
    })