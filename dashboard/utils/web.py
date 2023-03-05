from flask import jsonify

def json_data(data, status_code: int = 200):
    return jsonify({
        "status": status_code,
        "data": data
    })