from rrd import app
from flask import render_template, abort, request, url_for, redirect, g, jsonify
import os
import datetime
import json
import commands
from rrd.model.portal.log_record import LogRecorder
from rrd.model.portal.cmd_record import CMDRecorder


def reorder_list(oldlist, new_item):
    if new_item not in oldlist:
        return [new_item, oldlist[0], oldlist[1], oldlist[2], oldlist[3]]
    
    if new_item == oldlist[0]:
        return [new_item, oldlist[1], oldlist[2], oldlist[3], oldlist[4]]

    if new_item == oldlist[1]:
        return [new_item, oldlist[0], oldlist[2], oldlist[3], oldlist[4]]
    
    if new_item == oldlist[2]:
        return [new_item, oldlist[0], oldlist[1], oldlist[3], oldlist[4]]
    
    if new_item == oldlist[3]:
        return [new_item, oldlist[0], oldlist[1], oldlist[2], oldlist[4]]
    
    if new_item == oldlist[4]:
        return [new_item, oldlist[0], oldlist[1], oldlist[2], oldlist[3]]


@app.route('/portal/file_log')
def log_page():
    curr_row = LogRecorder.select_vs(where='username = %s', params=[g.user.name])
    if len(curr_row) == 0:
        history_paths = []
        return render_template(
            'portal/file_log/index.html', **locals()
        )
    else:
        curr_row = curr_row[0]
    history_paths_all = [curr_row.path1, curr_row.path2, curr_row.path3, curr_row.path4, curr_row.path5] 
    history_paths = []
    for path in history_paths_all:
        if path != '':
            history_paths.append(path)
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
        command = "tail -n 100 " + file_path + " | sed -r 's/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g'"
        log_history = commands.getoutput(command)
        if not os.path.isfile(file_path):
            log_history = "File not exist!"
        else:
            if LogRecorder.exists('username=%s', [g.user.name]):
                curr_row = LogRecorder.select_vs(where='username = %s', params=[g.user.name])[0]
                [path1, path2, path3, path4, path5] = reorder_list([curr_row.path1, curr_row.path2, curr_row.path3, curr_row.path4, curr_row.path5], file_path)
                
                LogRecorder.update_dict({
                'path1': path1,
                'path2': path2,
                'path3': path3,
                'path4': path4,
                'path5': path5,
                }, 'username=%s', [g.user.name])
            else:
                LogRecorder.insert({
                'username': g.user.name,
                'path1': file_path
                })
        ret["data"] = log_history
        ret['ok'] = True
        return json.dumps(ret)
    except Exception as e:
        abort(400, str(ret))


@app.route('/portal/bash_command')
def bash_command_page():
    curr_row = CMDRecorder.select_vs(where='username = %s', params=[g.user.name])
    if len(curr_row) == 0:
        history_cmds = []
        return render_template(
            'portal/bash_command/index.html', **locals()
        )
    else:
        curr_row = curr_row[0]
    history_cmds_all = [curr_row.command1, curr_row.command2, curr_row.command3, curr_row.command4, curr_row.command5]
    history_cmds = []
    for cmd in history_cmds_all:
        if cmd != '':
            history_cmds.append(cmd)
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
            if CMDRecorder.exists('username=%s', [g.user.name]):
                curr_row = CMDRecorder.select_vs(where='username = %s', params=[g.user.name])[0]
                
                [command1, command2, command3, command4, command5] = reorder_list([curr_row.command1, curr_row.command2, curr_row.command3, curr_row.command4, curr_row.command5], command)

                CMDRecorder.update_dict({
                'command1': command1,
                'command2': command2,
                'command3': command3,
                'command4': command4,
                'command5': command5,
                }, 'username=%s', [g.user.name])
            else:
                CMDRecorder.insert({
                'username': g.user.name,
                'command1': command
                })
            ret["data"] = command_result
            ret['ok'] = True
            return json.dumps(ret)
        else:
            ret["data"] = "Cannot execute command other than ls."
            ret['ok'] = True
            return json.dumps(ret)
    except Exception as e:
        abort(400, str(ret))

