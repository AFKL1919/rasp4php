from rasp.common.config import PROJECT_ROOT
from dashboard.core.webapp import WEBAPP
import json
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

config_file = PROJECT_ROOT / "resources" / "dashboard" / "config.json"
config_file_data = config_file.read_text()

CONFIG_DATA = json.loads(config_file_data)
WEBAPP.config["SQLALCHEMY_DATABASE_URI"] = CONFIG_DATA["WEBAPP"]["SQLALCHEMY_DATABASE_URI"]
