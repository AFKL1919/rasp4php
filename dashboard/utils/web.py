from rasp.core.app import RASP_APP
from dashboard.models.users import Users

from functools import wraps
from flask import jsonify, redirect, url_for, request, session, abort

def json_data(data, status_code: int = 200):
    return jsonify({
        "status": status_code,
        "data": data
    })

def not_install_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if RASP_APP.is_installed:
            return abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session["user_data"]
        if user is None:
            return redirect(url_for('login', next=request.url))
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session["user_data"]
        
        if user is None:
            return abort(403)
        
        user = Users(user)
        if user.permission != Users.ADMIN_USER:
            return abort(403)
        
        return f(*args, **kwargs)

    return decorated_function