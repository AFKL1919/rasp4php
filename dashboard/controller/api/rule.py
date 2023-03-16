from dashboard.core.webapp import WEBAPP
from dashboard.utils.web import json_data, admin_required, login_required
from rasp.core.rule import RULE_MANAGER

from flask import request


@WEBAPP.route("/api/rules", methods=["GET"])
@login_required
def get_rules():
    classname_and_rule_list_dict = RULE_MANAGER.get_all_rules()
    return json_data(classname_and_rule_list_dict.keys())


@WEBAPP.route("/api/rule", methods=["POST"])
@login_required
def get_rule_with_param():
    classname = request.form.get("classname")
    rule_type = request.form.get("rule_type", type=int, default=-1)

    rule_list = list()

    if classname == "":
        return json_data("缺少参数", 400)

    rule_obj_list = RULE_MANAGER.get_rule_list(classname)

    if rule_obj_list == list():
        return json_data("该过滤器不存在", 400)

    rule_list = [rule.serialize() for rule in rule_obj_list]

    if rule_type != -1:
        rule_list = list(filter(
            lambda rule: "rule_type" in rule and rule["rule_type"] == rule_type, rule_list
        ))

    return json_data({
        classname: rule_list
    })
