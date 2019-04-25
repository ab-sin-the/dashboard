from rrd import app
from flask import render_template, abort, request, url_for, redirect, g
import os
import datetime
import json

@app.route('/portal/log')
def log_page():

    return render_template(
        'portal/log/index.html', **locals()
    )


@app.route('/api/log_file')
def api_logfile():
    file_path = request.args.get("file")
    file_path = file_path.split()[0]
    command = "tail -n 100 " + file_path
    log_history = os.popen(command).read().encode().decode()
    log_history = log_history.replace('\n', '<br/>')
    if not os.path.isfile(file_path):
        log_history = "File not exist!"
    
        
    ret = {
            "ok": False,
            "data": "",
            }
    ret["data"] = log_history
    try:
        ret['ok'] = True
        return json.dumps(ret)
    except Exception as e:
        abort(400, str(ret))