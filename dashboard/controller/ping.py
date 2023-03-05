from dashboard.core.webapp import WEBAPP

@WEBAPP.route("/ping")
def ping():
    return "pong"
