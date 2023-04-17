from dashboard.core.webapp import WEBAPP
from dashboard.core.db import DB_SESSION
from dashboard.models.users import Users
from dashboard.utils.web import json_data, admin_required, not_install_required, login_required

from flask import session, request


@WEBAPP.route("/api/user/update", methods=["POST"])
@admin_required
def update_info():
    username = request.form.get("username")
    new_password = request.form.get("new_password")

    if isinstance(new_password, str) and isinstance(username, str):
        user = Users.query.filter(
            Users.username == username
        ).update({
            'password': new_password
        })
        DB_SESSION.commit()
    else:
        return json_data("输入格式错误", 400)

    if user.id == None:
        return json_data("用户信息修改失败", 500)

    return json_data("用户信息修改成功", 200)


@WEBAPP.route("/api/user/admin_register", methods=["POST"])
@not_install_required
def register_admin():
    username = request.form.get("username")
    password = request.form.get("password")

    if isinstance(password, str) and isinstance(username, str):
        user = Users(username, password, Users.ADMIN_USER)
    else:
        return json_data("输入格式错误", 400)

    if user != None:
        DB_SESSION.add(user)
        DB_SESSION.commit()
    else:
        return json_data("用户添加失败，请更换用户名！", 400)

    if user.id == None:
        return json_data("用户添加失败", 500)

    session["user_data"] = user.serialize()

    return json_data("用户添加成功", 200)


@WEBAPP.route("/api/user/register", methods=["POST"])
@admin_required
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    permission = request.form.get("permission", type=int)

    if isinstance(password, str) and isinstance(username, str):
        user = Users.register(username, password, permission)
    else:
        return json_data("输入格式错误", 400)

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
        password = Users.hash_user_password(password)
    else:
        return json_data("输入格式错误", 400)

    user = Users.query.filter(
        Users.username == username,
        Users.password == password
    ).first()

    if not isinstance(user, Users):
        return json_data("登录失败", 401)

    session["user_data"] = user.serialize()

    return json_data("登录成功")


@WEBAPP.route("/api/user/info", methods=["GET"])
@login_required
def current_user_info():
    result = {
        "username": session["user_data"]["username"],
        "permission": session["user_data"]["permission"]
    }

    return json_data(result)


@WEBAPP.route("/api/user", methods=["GET"])
@login_required
def all_user_data():
    
    users = DB_SESSION.query(
        Users.id, Users.username, Users.permission
    ).all()

    result = [
        {
            "id": user.id, 
            "username": user.username, 
            "permission": "admin" if user.permission == Users.ADMIN_USER else "user"
        } for user in users
    ]

    return json_data(result)
