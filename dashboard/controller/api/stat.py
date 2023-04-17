from dashboard.core.webapp import WEBAPP
from dashboard.utils.web import json_data, login_required
from dashboard.models.message import Message
from dashboard.core.db import DB_SESSION
from rasp.core.hooks import HooksManager

from sqlalchemy import func, DateTime, desc
from datetime import datetime, date, time, timedelta

DATETIME_FORMAT = "%Y-%m-%d"

@WEBAPP.route("/api/stat/alarm/time", methods=["POST"])
# @login_required
def get_alarm_log_count_by_time():

    today = date.today()
    last_s = time(23, 59, 59)
    delta = timedelta(days=1)

    end_date_time = datetime.combine(today, last_s)
    start_date_time = end_date_time - timedelta(days=14)

    msg_count_query = DB_SESSION.query(
        func.date_trunc(
            'day', Message.time
        ).cast(DateTime).label('day'),
        func.count(1)
    ).filter(
        Message.time.between(
            start_date_time, end_date_time
        )
    ).group_by('day')

    result = dict(msg_count_query.all())
    result = {
        dt.date(): count 
        for dt, count in result.items()
    }

    current_date_time = end_date_time
    while current_date_time >= start_date_time:
        current_date = current_date_time.date()

        if current_date not in result:
            result[current_date] = 0

        current_date_time -= delta

    result = {
        dt.strftime(DATETIME_FORMAT): count 
        for dt,count in result.items()
    }

    resp = json_data(result)
    resp.headers.add("Access-Control-Allow-Origin", "*")
    return resp


@WEBAPP.route("/api/stat/alarm/type", methods=["POST"])
# @login_required
def get_alarm_log_count_by_type():

    msg_count_query = Message.query.with_entities(
        Message.type,
        func.count(Message.type)
    ).group_by(
        Message.type
    )

    result = dict(msg_count_query.all())
    for type_name, _ in HooksManager.hooks.items():
        if type_name not in result:
            result[type_name] = 0

    resp = json_data(result)
    resp.headers.add("Access-Control-Allow-Origin", "*")
    return resp


@WEBAPP.route("/api/stat/alarm/remote_addr", methods=["POST"])
# @login_required
def get_alarm_log_count_by_remote_addr():


    msg_count_query = Message.query.with_entities(
        Message.remote_addr,
        func.count(Message.remote_addr).label('count_addr')
    ).group_by(
        Message.remote_addr
    ).order_by(desc('count_addr')).limit(6)

    result = dict(msg_count_query.all())
    resp = json_data(result)
    resp.headers.add("Access-Control-Allow-Origin", "*")
    return resp

@WEBAPP.route("/api/test", methods=["GET"])
def test_data():
    msg = {
        'pid': 11,
        'function': 'file_get_contents',
        'args': ['/etc/passwd'],
        'normalized_args': ['/etc/passwd'],
        'filename': '/usr/share/nginx/html/file.php',
        'lineno': 2,
        'context': 'file',
        'type': 'file_operation',
        'request_uri': '/file.php?1=%2Fetc%2Fpasswd',
        'remote_addr': '172.18.0.1',
        'query_string': '1=%2Fetc%2Fpasswd',
        'document_root': '/usr/share/nginx/html',
        'hook_point': 'php_stream_locate_url_wrapper'
    }

    from random import randint
    from datetime import timedelta
    def get_random_ip():
        ip_list = [
            '172.18.0.1',
            '172.19.0.2',
            '192.168.12.7',
            '172.18.0.122',
            '114.114.114.114',
            '8.8.8.8',
            '114.19.195.14'
        ]
        ip_list_len = len(ip_list)
        return ip_list[randint(0, ip_list_len-1)]

    def get_random_time():
        now = datetime.now()
        time_list = [
            now - timedelta(days=1), now - timedelta(days=2), now - timedelta(days=3),
            now - timedelta(days=4), now - timedelta(days=5), now - timedelta(days=6),
            now - timedelta(days=7), now - timedelta(days=8), now - timedelta(days=9),
            now - timedelta(days=10), now - timedelta(days=11), now - timedelta(days=12),
            now - timedelta(days=13), now - timedelta(days=14)
        ]
        time_list_len = len(time_list)
        return time_list[randint(0, time_list_len-1)]

    def set_m(msg):
        m = Message(msg)
        m.time = get_random_time()
        DB_SESSION.add(m)

    for _ in range(10):
        msg['remote_addr'] = get_random_ip()
        set_m(msg)

    msg['pid'] = 9
    msg['type'] = 'command_execution'
    msg['context'] = 'command'
    msg['hook_point'] = 'zif_popen'
    for _ in range(5):
        msg['remote_addr'] = get_random_ip()
        set_m(msg)

    msg['hook_point'] = 'php_exec'
    for _ in range(6):
        msg['remote_addr'] = get_random_ip()
        set_m(msg)
    
    msg['pid'] = 10
    msg['type'] = 'database_operation'
    msg['context'] = 'sql'
    msg['hook_point'] = 'php_mysqlnd_cmd_write'
    for _ in range(6):
        msg['remote_addr'] = get_random_ip()
        set_m(msg)
    
    msg['pid'] = 10
    msg['type'] = 'code_execution'
    msg['context'] = 'code'
    msg['hook_point'] = 'compile_string'
    for _ in range(2):
        msg['remote_addr'] = get_random_ip()
        set_m(msg)
    
    DB_SESSION.commit()

    return json_data("test data inserted")