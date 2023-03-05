from dashboard.core.webapp import WEBAPP
from dashboard.core.db import DB_SESSION
from dashboard.utils.web import json_data
from dashboard.models.users import Users

from rasp.core.app import RASP_APP
from rasp.core.script import script_context_manager

from flask import session, request

@WEBAPP.route("/api/register", method=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    permission = request.form.get("permission", type=int)

    if isinstance(password, str) and isinstance(username, str):
        password = Users.user_password_hash(password)
    else:
        return json_data("输入格式错误", 400)
    
    user = Users(username, password, permission)
    DB_SESSION.add(user)
    DB_SESSION.commit()

    if user.id == None:
        return json_data("用户添加失败", 500)

    return json_data("用户添加成功", 200)

@WEBAPP.route("/api/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if isinstance(password, str) and isinstance(username, str):
        password = Users.user_password_hash(password)
    else:
        return json_data("输入格式错误", 400)

    user = Users.query.filter(
        Users.username == username,
        Users.password == password
    ).first()

    if not isinstance(user, Users):
        return json_data("登录失败", 401)

    session["user_data"] = user
    return json_data("登录成功")