from rrd import app
from flask import render_template, abort, request, url_for, redirect, g
import os
import datetime
import json
import commands


last_five_queries = []
last_five_cmd = []

@app.route('/portal/file_log')
def log_page():
    history_paths = last_five_queries
    return render_template(
        'portal/file_log/index.html', **locals()
    )

@app.route('/api/log_file')
def api_logfile():    
    ret = {
            "ok": False,
            "data": "",
            }
    try:
        file_path = request.args.get("file")
        if len(file_path.split()) == 0:
            log_history = "File not exist!"
            ret["data"] = log_history
            ret['ok'] = True
            return json.dumps(ret)
        file_path = file_path.split()[0]
        command = "tail -n 100 " + file_path
        log_history = commands.getoutput(command)
        if not os.path.isfile(file_path):
            log_history = "File not exist!"
        else:
            if file_path not in last_five_queries:
                last_five_queries.append(file_path)
        ret["data"] = log_history
        ret['ok'] = True
        return json.dumps(ret)
    except Exception as e:
        abort(400, str(ret))


@app.route('/portal/bash_command')
def bash_command_page():
    history_cmd = last_five_cmd
    return render_template(
        'portal/bash_command/index.html', **locals()
    )

@app.route('/api/execute_command')
def api_execute_command():
        
    ret = {
            "ok": False,
            "data": "",
            }
    try:
        command = request.args.get("command")
        if command.split()[0] == "ls":
            command_result = commands.getoutput(command)  
            if command not in last_five_cmd:
                last_five_cmd.append(command)  
            ret["data"] = command_result
            ret['ok'] = True
            return json.dumps(ret)
        else:
            ret["data"] = "Cannot execute command other than ls."
            ret['ok'] = True
            return json.dumps(ret)
    except Exception as e:
        abort(400, str(ret))