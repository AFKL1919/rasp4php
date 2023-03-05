from dashboard.core.webapp import WEBAPP
from dashboard.core.db import DB_SESSION
from dashboard.models.users import Users
from dashboard.utils.web import json_data, admin_required, not_install_required

from flask import session, request

@WEBAPP.route("/api/user/update", method=["POST"])
@admin_required
def update_info():
    username = request.form.get("username")
    new_password = request.form.get("new_password")

    if isinstance(new_password, str) and isinstance(username, str):
        new_password = Users.user_password_hash(new_password)
    else:
        return json_data("输入格式错误", 400)
    
    user = Users.query.filter(
        Users.username == username
    ).update({
        'password': new_password
    })
    DB_SESSION.commit()

    if user.id == None:
        return json_data("用户添加失败", 500)

    return json_data("用户添加成功", 200)

@WEBAPP.route("/api/user/admin_register", method=["POST"])
@not_install_required
def register_admin():
    username = request.form.get("username")
    password = request.form.get("password")

    if isinstance(password, str) and isinstance(username, str):
        password = Users.user_password_hash(password)
    else:
        return json_data("输入格式错误", 400)
    
    user = Users(username, password, Users.ADMIN_USER)
    DB_SESSION.add(user)
    DB_SESSION.commit()

    if user.id == None:
        return json_data("用户添加失败", 500)
    
    session["user_data"] = user

    return json_data("用户添加成功", 200)


@WEBAPP.route("/api/user/register", method=["POST"])
@admin_required
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

@WEBAPP.route("/api/user/login", methods=["POST"])
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