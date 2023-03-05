from __future__ import unicode_literals
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
config_file = PROJECT_ROOT / "resources" / "dashboard" / "config.json"

__VERSION__ = '0.6.1'
APPLICATION_NAME = "RASP4PHP"

RASP_APP_ROOT = PROJECT_ROOT / "rasp"
DASHBOARD_ROOT = PROJECT_ROOT / "dashboard"
RESOURCES_ROOT = PROJECT_ROOT / "resources"

RASP_APP_RESOURCES = RESOURCES_ROOT / "rasp"
DASHBOARD_RESOURCES = RESOURCES_ROOT / "dashboard"