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

lynis_workdir = "/home/absinthe/Projects/lynis"
GScan_workdir = "/home/absinthe/Projects/GScan"

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
    try:
        audit_method = request.args.get("audit_method")
        if audit_method == "lynis":
            command = "cd " + lynis_workdir + " && ./lynis audit system  | sed -r 's/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K|C]//g'"
            print(command)
            command_result = commands.getoutput(command)
        elif audit_method == "GScan":
            command = "cd " + GScan_workdir + " && python GScan.py  | sed -r 's/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K|C]//g'"
            print(command)
            command_result = commands.getoutput(command)
        ret["data"] = command_result
        ret['ok'] = True
        return json.dumps(ret)
    except Exception as e:
        abort(400, str(ret))

