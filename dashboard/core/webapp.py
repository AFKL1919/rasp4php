from flask import Flask
from rasp.utils.log import logger
from rasp.common.config import APPLICATION_NAME, DASHBOARD_RESOURCES

WEBAPP = Flask(
    APPLICATION_NAME, 
    template_folder=DASHBOARD_RESOURCES / "template"
)

def web_app_start(host: str, port: int):
    import dashboard.controller
    WEBAPP.run(host, port, debug=False)