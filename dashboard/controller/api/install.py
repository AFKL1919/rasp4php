from dashboard.core.webapp import WEBAPP
from dashboard.utils.web import json_data
from rasp.core.app import RASP_APP


@WEBAPP.route("/api/install", methods=["GET"])
def start_install():
    
    if not RASP_APP.is_installed:
        try:
            RASP_APP.start()
            
        except Exception as e:

            RASP_APP.is_installed = False
            WEBAPP.logger.exception(e)
            return json_data({
                "status": 500,
                "data": {
                    "msg": "{}".format(e),
                    "is_installed": RASP_APP.is_installed
                }
            })
    
    return json_data({
        "status": 200,
        "data": {
            "is_installed": RASP_APP.is_installed
        }
    })