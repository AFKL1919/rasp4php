from rasp.core.app import RASP_APP
from dashboard.core.webapp import WEBAPP
from rasp.common.config import DASHBOARD_RESOURCES
from dashboard.utils.web import not_install_required, login_required

from flask import render_template, send_from_directory, redirect


@WEBAPP.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(
        DASHBOARD_RESOURCES / "template/css", path
    )


@WEBAPP.route('/script/<path:path>')
def send_script(path):
    return send_from_directory(
        DASHBOARD_RESOURCES / "template/script", path
    )


@WEBAPP.route('/component/<path:path>')
def send_component(path):
    return send_from_directory(
        DASHBOARD_RESOURCES / "template/component", path
    )


@WEBAPP.route("/login.html")
@WEBAPP.route("/login")
def login_page():
    if not RASP_APP.is_installed:
        return redirect("/install.html")

    return render_template("login.html")


@WEBAPP.route("/install.html")
@WEBAPP.route("/install")
@not_install_required
def install_page():
    return render_template("install.html")


@WEBAPP.route("/index.html")
@WEBAPP.route("/index")
@WEBAPP.route("/")
@login_required
def index_page():
    return render_template("index.html")


@WEBAPP.route("/rasp-log.html")
@login_required
def rasp_log_page():
    return render_template("rasp-log.html")


@WEBAPP.route("/ip-controller.html")
@login_required
def ip_con_page():
    return render_template("ip-controller.html")
    

@WEBAPP.route("/file-controller.html")
@login_required
def file_con_page():
    return render_template("file-controller.html")


@WEBAPP.route("/users.html")
@login_required
def user_data_page():
    return render_template("users.html")

@WEBAPP.route("/user.html")
@login_required
def current_user_info_page():
    return render_template("user.html")