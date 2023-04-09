from rasp.utils.log import logger
from dashboard.core.webapp import WEBAPP

from time import sleep
from flask_sqlalchemy import SQLAlchemy

DB_BASE = SQLAlchemy(
    WEBAPP, 
    session_options={
        "expire_on_commit": False
    }
)

MAX_RETRIES = 6

for i in range(MAX_RETRIES):
    try:
        with WEBAPP.app_context():
            DB_BASE.engine.connect()
    except Exception as ex:
        logger.error(f"Failed to connect. Try again: {ex}")
        sleep(2)
    else:
        break
else:
    raise Exception("Failed to connect to database after maximum retries")

DB_SESSION = DB_BASE.session
DB_BASE.init_app(WEBAPP)

def init_db():
    try:
        import dashboard.models
        with WEBAPP.app_context():
            DB_BASE.create_all()
    except Exception as e:
        logger.exception(e)

init_db()