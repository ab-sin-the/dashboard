# -*- coding:utf-8 -*-
# Copyright 2017 Xiaomi, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = 'Yiwen Chen'
from rrd import app
from flask import request, g, render_template, jsonify, abort
import json
import time
import commands
import subprocess
import os

lynis_workdir = "/home/work/open-falcon/lynis"
GScan_workdir = "/home/work/open-falcon/GScan"

def check_running(script_name):
    command = "ps -ef | grep " + script_name + " | grep -v grep | wc -l"
    proc_num = commands.getoutput(command)
    if int(proc_num) != 0:
        return True
    return False

@app.route('/portal/security_audit')
def security_audit_get():
    return render_template(
        'portal/security_audit/index.html'
    )


@app.route('/api/security_audit')
def execute_audit():
    ret = {
            "ok": False,
            "data": "",
            }
    ret["data"] = ""


    try:
        audit_method = request.args.get("audit_method")
        if check_running(audit_method) == True:
            ret['ok'] = True
            ret["data"] = "is running"
            return json.dumps(ret)
        if audit_method == "lynis":
            command = "cd " + lynis_workdir + " && ./lynis audit system  | sed -r 's/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K|C]//g' > report/lynis_report"
            print(command)
            subprocess.Popen(command, shell=True)
        elif audit_method == "GScan":
            command = "cd " + GScan_workdir + " && python GScan.py  | sed -r 's/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K|C]//g' > report/GScan_report"
            print(command)
            subprocess.Popen(command, shell=True)
        ret['ok'] = True
        return json.dumps(ret)
    except Exception as e:
        abort(400, str(ret))


@app.route('/api/security_report')
def get_report():
    ret = {
            "ok": False,
            "data": "",
            }
    try:
        audit_method = request.args.get("audit_method")
        if audit_method == "lynis":
            command = "cat " + lynis_workdir + "/report/lynis_report"
            print(command)
            command_res = commands.getoutput(command)
        elif audit_method == "GScan":
            command = "cat " + GScan_workdir + "/report/GScan_report"
            print(command)
            command_res = commands.getoutput(command) 
        ret["data"] = command_res
        ret['ok'] = True
        return json.dumps(ret)
    except Exception as e:
        abort(400, str(ret))
