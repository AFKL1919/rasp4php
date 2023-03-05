from __future__ import unicode_literals
import json

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent

RASP_APP_ROOT = PROJECT_ROOT / "rasp"
DASHBOARD_ROOT = PROJECT_ROOT / "dashboard"
RESOURCES_ROOT = PROJECT_ROOT / "resources"

RASP_APP_RESOURCES = RESOURCES_ROOT / "rasp"
DASHBOARD_RESOURCES = RESOURCES_ROOT / "dashboard"

config_file = PROJECT_ROOT / "resources" / "rasp" / "config.json"
config_file_data = config_file.read_text()

CONFIG_DATA = json.loads(config_file_data)

__VERSION__ = CONFIG_DATA["RASP_CONFIG"]["VERSION"]
APPLICATION_NAME = CONFIG_DATA["RASP_CONFIG"]["APPLICATION_NAME"]
