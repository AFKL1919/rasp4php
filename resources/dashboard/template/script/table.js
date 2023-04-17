import { CONFIG } from "./config.js";
var url = CONFIG.DASHBOARD_API_URL;

function init_table(doc_id, dataSet, option = {}, event = (table) => { }) {
    $(document).ready(function () {
        var table = $(doc_id).DataTable({
            data: dataSet,
            ...option
        });

        event(table);
    });
}

function user_table_event(table) {
    $(document).ready(function () {
        $('#dataTable tbody').on('click', 'tr', function () {

            $(this).toggleClass('selected');

            var user_row = table.rows('.selected').data()[0];
            var id = user_row["id"];
            var username = user_row["username"];
            var permission = user_row["permission"];

            $(this).toggleClass('selected');

            $('#UserModalLabel').text("用户修改");

            $('#user-id').val(id);
            $('#username').val(username);

            var options = $('#permission option');
            for (var option of options) {
                if (option.value == permission) {
                    $(option).prop("selected", true);
                    break;
                }
            }

            $('#UserModal').modal();
        });

        $('#confirm').on('click', function () {

            var user_id = $("#user-id").val();
            var username = $("#username").val();
            var password = $("#password").val();
            var permission = ($("#permission").val() == "admin") ? 1 : 0;

            $.ajax({
                url: `${url}/api/user/update`,
                type: 'POST',
                data: {
                    "user_id": user_id,
                    "username": username,
                    "new_password": password,
                    "permission": permission
                },
                success: function (data) {
                    if (data["status"] == 200) {
                        alert("修改成功");
                        location.reload();
                    } else {
                        alert("修改失败");
                    }
                },
                error: function () {
                    alert("修改失败");
                }
            });
        });
    });
}

function ip_rule_table_event(table) {
    $(document).ready(function () {
        $('#dataTable tbody').on('click', 'tr', function () {

            $(this).toggleClass('selected');

            var ip_rule_row = table.rows('.selected').data()[0];
            var id = ip_rule_row["id"];
            var data = ip_rule_row["data"];
            var rule_type = ip_rule_row["rule_type"];

            $(this).toggleClass('selected');

            $('#IPRuleModalLabel').text("IP规则修改");

            $('#ip-rule-id').val(id);
            $('#ip-rule-data').val(data);

            var org_rule_type = (rule_type == "黑名单") ? 1 : 0;
            var options = $('#rule-type option');
            for (var option of options) {
                if (option.value == org_rule_type) {
                    $(option).prop("selected", true);
                    break;
                }
            }

            $('#IPRuleModal').modal();
        });

        $('#confirm').on('click', function () {

            var rule_id = $('#ip-rule-id').val();
            var rule_data = $('#ip-rule-data').val();
            var rule_type = $('#rule-type').val();

            $.ajax({
                url: `${url}/api/rule/update`,
                type: 'POST',
                data: {
                    rule_id: rule_id,
                    data: rule_data,
                    rule_type: rule_type,
                    classname: 'DefaultUserIPFilter',
                },
                success: function (data) {
                    if (data["status"] == 200) {
                        alert("修改成功");
                        location.reload();
                    } else {
                        alert("修改失败");
                    }
                },
                error: function () {
                    alert("修改失败");
                }
            });
        });
    });
}

function file_rule_table_event(table) {
    $(document).ready(function () {
        $('#dataTable tbody').on('click', 'tr', function () {

            $(this).toggleClass('selected');

            var ip_rule_row = table.rows('.selected').data()[0];
            var id = ip_rule_row["id"];
            var data = ip_rule_row["data"];
            var rule_type = ip_rule_row["rule_type"];

            $(this).toggleClass('selected');

            $('#FileRuleModalLabel').text("文件规则修改");

            $('#file-rule-id').val(id);
            $('#file-rule-data').val(data);

            var org_rule_type = (rule_type == "黑名单") ? 1 : 0;
            var options = $('#rule-type option');
            for (var option of options) {
                if (option.value == org_rule_type) {
                    $(option).prop("selected", true);
                    break;
                }
            }

            $('#FileRuleModal').modal();
        });

        $('#confirm').on('click', function () {

            var rule_id = $('#ip-rule-id').val();
            var rule_data = $('#ip-rule-data').val();
            var rule_type = $('#rule-type').val();

            $.ajax({
                url: `${url}/api/rule/update`,
                type: 'POST',
                data: {
                    rule_id: rule_id,
                    data: rule_data,
                    rule_type: rule_type,
                    classname: 'DefaultFileFilter',
                },
                success: function (data) {
                    if (data["status"] == 200) {
                        alert("修改成功");
                        location.reload();
                    } else {
                        alert("修改失败");
                    }
                },
                error: function () {
                    alert("修改失败");
                }
            });
        });
    });
}


export { init_table, user_table_event, ip_rule_table_event, file_rule_table_event };