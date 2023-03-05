from dashboard.core.webapp import WEBAPP

import json
from os import urandom
from datetime import timedelta

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
config_file = PROJECT_ROOT / "resources" / "dashboard" / "config.json"
config_file_data = config_file.read_text()

CONFIG_DATA = json.loads(config_file_data)

WEBAPP.config["SECRET_KEY"] = urandom(32) if CONFIG_DATA["APP_CONFIG"]["SECRET_KEY"] == "" else CONFIG_DATA["APP_CONFIG"]["SECRET_KEY"]
WEBAPP.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=CONFIG_DATA["APP_CONFIG"]["PERMANENT_SESSION_LIFETIME"])
WEBAPP.config["SQLALCHEMY_DATABASE_URI"] = CONFIG_DATA["DB"]["SQLALCHEMY_DATABASE_URI"]
