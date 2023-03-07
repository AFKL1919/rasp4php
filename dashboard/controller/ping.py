from dashboard.core.webapp import WEBAPP
from dashboard.utils.web import json_data

@WEBAPP.route("/ping")
def ping():
    return json_data("pong")