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
import re
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

@app.route('/portal/access_detect')
def access_detect_get():
    return render_template(
        'portal/access_detect/index.html'
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



def generate_sub_keyword(keyword, color):
    keyword_sub = '</pre>'
    if color == 'red':
        bg_color = 'rgba(221, 77, 84, 1)'
    elif color == 'blue':
        bg_color = 'rgba(36, 95, 240, 1)'
    elif color == 'green':
        bg_color = 'rgba(0, 181, 91, 1)'

    keyword_sub = keyword_sub + ' <span style = "height:16px; background:' + bg_color + '; border-radius:2px; padding: 1px 13px; font-size:10px; font-family:PingFangSC-Semibold; font-weight:600; color:rgba(255,255,255,1);line-height:14px;"> ' + keyword + '</span><br/>' + '<pre  class="audit-display-pre">'
    return keyword_sub 


def replace_found(value):
    keyword = value.group()
    keyword = keyword[2:]
    keyword = keyword[:-2]
    return generate_sub_keyword(keyword, 'green')
    

def replace_key_word(new_command_res, keyword, color):
    if keyword == 'FOUND':
        re_expr = r'\[ ' + keyword + r' \]'
        re_expr2 = r'\[ \d+ ' + keyword + r' \]'
        re_expr3 = r'\[ ' + keyword + r' \(\d+\) \]'
        new_command_res = re.sub(re_expr3, replace_found, new_command_res)
        new_command_res = re.sub(re_expr2, replace_found, new_command_res)
    else: 
        re_expr = r'\[ ' + keyword + r' \]'
    
    new_command_res = re.sub(re_expr, generate_sub_keyword(keyword, color) , new_command_res)
    return new_command_res

header_num = 0

def generate_header(value):
    global header_num
    header_name = value.group()
    header_name = header_name[4:]
    header_name = header_name[:-37]
    header_str = '</pre></div><hr style="margin: 0px 0px 13px 0px;"><div id="report_part_'+ str(header_num) + '"> <span class="report-dropdown pull-right" onclick="report_display_single(' + str(header_num) + ')"><img src="/static/img/dropdown.svg"></span> <div class = "visual_report_header" id="report_head_part_'+ str(header_num) +'">'
    header_str = header_str + header_name
    header_str = header_str + '</div><pre class="audit-display-pre">'
    header_num = header_num + 1
    return header_str

def count_num(result_each):
    combined_result = ""
    for result in result_each:
        num = result.count("rgba(221, 77, 84, 1)")
        if num == 0:
            combined_result = combined_result + result + '<hr style="margin:15px 0px;">'
        else:
            result_end_index = result.find('</div>')
            new_result = result[:result_end_index] + '<span class="problem-num">' + str(num) + "</span>" +result[result_end_index:]
            combined_result = combined_result + new_result + '<hr style="margin:15px 0px;">'
    return combined_result

def visualize_title(result):
    global header_num
    header_num = 1
    re_expr_2 = r'\[ Lynis 2.7.4 \]'
    re_expr_3 = r'=+\n*  \-\[ Lynis 2.7.4 Results \]\-'
    re_expr = r'\[\+\].*([\n])\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-'
    result = re.sub(re_expr_2,'</pre><div class = "visual_report_header" id="report_head_part_0' + '" style="margin-bottom:0px;"> Lynis 2.7.4 </div><pre class="audit-display-pre">' , result)
    result = re.sub(re_expr, generate_header, result)
    result = re.sub(re_expr_3,'</pre> </div><hr style="margin: 0px 0px 13px 0px;">  <div id="report_part_'+ str(header_num) + '"> <span class="report-dropdown pull-right" onclick="report_display_single(' + str(header_num) + ')"><img src="/static/img/dropdown.svg"></span> <div class = "visual_report_header" id="report_head_part_'+ str(header_num) +'"> Lynis 2.7.4 Result </div><pre class="audit-display-pre">' , result)
    result_each = result.split('<hr style="margin: 0px 0px 13px 0px;">')
    result = count_num(result_each)
    return result

def visualize_lynis_report(command_res):
    keyword_list = ['DONE', 'ENABLED', 'DISABLED', 'NOT ENABLED', 'PROTECTED', 'UNKNOWN', 'NONE', 'WEAK', 'INSTALLED', 'FOUND', 'NOT FOUND', 'OK', 'DIFFERENT' , 'WARNING', 'RUNNING', 'NOT RUNNING', 'SUGGESTION', 'NOT DISABLED', 'SKIPPED', 'ACTIVE', 'NO', 'FILES FOUND', 'NOT ACTIVE', 'ACCEPT', 'YES', 'DEFAULT', 'systemd']
    color = ['green', 'green', 'red', 'red', 'green', 'blue', 'green', 'red', 'green', 'green', 'blue', 'green', 'red', 'red', 'green', 'red', 'blue', 'green', 'green', 'green', 'blue', 'blue', 'red', 'green', 'green', 'green', 'green']
    new_command_res = command_res
    for keyword_id in range(len(keyword_list)):
        new_command_res = replace_key_word(new_command_res, keyword_list[keyword_id], color[keyword_id])
    new_command_res = visualize_title(new_command_res)
    return '<div id="report_part_0"><span class="report-dropdown pull-right" onclick="report_display_single(' + str(0) + ')"><img src="/static/img/dropdown.svg"></span><pre class="audit-display-pre">' + new_command_res + '</div>'


def get_lynis_detail(detail_type):
    command = "cat " + lynis_workdir + "/report/lynis_report"
    command_res = commands.getoutput(command)
    if detail_type == 'report':
        return command_res
    elif detail_type == 'visual_report':
        return visualize_lynis_report(command_res)
    else:
        details = command_res.split("================================================================================")
        problem_details = details[1]
        problem_details = problem_details.split('----------------------------')
        warnings = problem_details[1].split('Suggestions')[0]
        suggestion = problem_details[2].split('Follow-up:')[0]
        if detail_type == 'warning':
            return warnings
        elif detail_type == 'suggestion':
            return suggestion
        return "finished"

def get_Gscan_detail(detail_type):
    command = "cat " + GScan_workdir + "/report/GScan_report"
    command_res = commands.getoutput(command) 
    if detail_type == 'report':
        return command_res
    else:
        problems_detail = command_res.split('------------------------------\n')[1]
        if detail_type == 'all':
            return problems_detail
        else:
            if problems_detail.index('[1][可疑]') != -1:
                entry_info = problems_detail.split('[1][可疑]')[0]
                vulun_poss = '[1][可疑]' + problems_detail.split('[1][可疑]')[1]
            elif problems_detail.index('[1][风险]') != -1:
                entry_info = problems_detail.split('[1][风险]')[0]
                vulun_poss = '[1][风险]' + problems_detail.split('[1][风险]')[1]
            else:
                entry_info = problems_detail
                vulun_poss = ""
            
            if detail_type == 'entry_info':
                return entry_info
            else:
                return vulun_poss


@app.route('/api/security/detail_report')
def get_detail_report():
    ret = {
        "ok": False,
        "data": "",
    }
    try:
        audit_method = request.args.get("audit_method")
        detail_type = request.args.get("detail_type")
        if audit_method == "lynis":
            res = get_lynis_detail(detail_type)
        elif audit_method == "GScan":
            res = get_Gscan_detail(detail_type)
            
        ret["data"] = res
        ret['ok'] = True
        return json.dumps(ret)
    except Exception as e:
        abort(400, str(ret))