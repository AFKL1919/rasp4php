from dashboard.core.webapp import WEBAPP
from rasp.core.app import RASP_APP
from dashboard.utils.web import json_data, not_install_required, admin_required


@WEBAPP.route("/api/install", methods=["GET"])
@not_install_required
@admin_required
def start_install():
    
    if not RASP_APP.is_installed:
        try:
            RASP_APP.start()
            
        except Exception as e:

            RASP_APP.is_installed = False
            WEBAPP.logger.exception(e)
            return json_data({
                "msg": "{}".format(e),
                "is_installed": RASP_APP.is_installed
                },
                500
            )
    
    return json_data({
        "is_installed": RASP_APP.is_installed
    })