from dashboard.core.webapp import WEBAPP
from dashboard.core.db import DB_SESSION
from dashboard.utils.web import json_data, admin_required, login_required
from rasp.core.rule import RULE_MANAGER
from rasp.core.filter import FILTER_MANAGER
from rasp.utils.log import logger
from rasp.common.config import Path

from flask import request, send_file


@WEBAPP.route("/api/rules", methods=["GET"])
@login_required
def get_rules():

    classname_and_rule_data_list_dict = dict()
    classname_and_rule_obj_list_dict = RULE_MANAGER.get_all_rules()

    for classname in classname_and_rule_obj_list_dict.keys():

        rule_obj_list = classname_and_rule_obj_list_dict[classname]
        rule_data_list = [rule.serialize() for rule in rule_obj_list]
        classname_and_rule_data_list_dict[classname] = rule_data_list

    return json_data(classname_and_rule_data_list_dict)


@WEBAPP.route("/api/rule", methods=["POST"])
@login_required
def get_rule_with_param():
    classname = request.form.get("classname")
    rule_type = request.form.get("rule_type", type=int, default=-1)

    rule_list = list()

    if classname == "":
        return json_data("缺少参数", 400)

    rule_obj_list = RULE_MANAGER.get_rule_list(classname)

    if not rule_obj_list:
        return json_data("该过滤器不存在", 400)

    rule_list = [rule.serialize() for rule in rule_obj_list]

    if rule_type != -1:
        rule_list = list(filter(
            lambda rule: "rule_type" in rule and rule["rule_type"] == rule_type, rule_list
        ))

    return json_data(rule_list)

@WEBAPP.route("/api/rule/update", methods=["POST"])
@admin_required
def update_rule_by_params():
    classname = request.form.get("classname")
    rule_id = request.form.get("rule_id", type=int)

    if classname == "":
        return json_data("缺少参数", 400)
    
    filter_instance = FILTER_MANAGER.get_filter_with_name(classname)
    rule_method = filter_instance.rule_method
    
    try:
        rule = DB_SESSION.query(rule_method).get(rule_id)
        col_list = rule_method.__table__.columns.keys()

        for col in col_list:
            col_data = request.form.get(col, default=None)
            
            if col == "id" or col_data == None:
                continue

            setattr(rule, col, col_data)
        
        DB_SESSION.commit()

        RULE_MANAGER.update_rule(rule_method, classname)
        filter_instance.update_filter_rule()
        
    except Exception as e:
        return json_data(str(e), 500)
    
    logger.info(f"filter rules changed Filter:{classname} rules:{[rule.serialize() for rule in RULE_MANAGER.get_rule_list(classname)]}")
    return json_data("修改成功")


@WEBAPP.route("/api/rule/dump", methods=["POST"])
@login_required
def dump_rule_with_param():
    classname = request.form.get("classname")
    
    try:
        path = RULE_MANAGER.dump_rules_to_file(classname)
    except Exception as e:
        return json_data({"msg":"error"}, 500)

    return json_data(f"成功导出至：{str(path)}")


@WEBAPP.route("/api/rule/download", methods=["POST"])
@login_required
def download_rule_with_param():
    classname = request.form.get("classname")
    rule_obj_list = RULE_MANAGER.get_rule_list(classname)

    if not rule_obj_list:
        return json_data("该过滤器不存在", 400)
    
    file = Path(rule_obj_list[0].filename)
    if not file.is_file():
        logger.error(f"导出规则文件失败，文件名：{str(file)}")
        return json_data("下载失败", 500)
    
    return send_file(str(file))