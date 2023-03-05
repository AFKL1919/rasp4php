from flask_sqlalchemy import SQLAlchemy

from rasp.utils.log import logger
from dashboard.core.webapp import WEBAPP

DB_BASE = SQLAlchemy(WEBAPP)
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