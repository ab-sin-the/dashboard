# -*- coding: utf-8 -*-  
from rrd import app
from flask import render_template, abort, request, url_for, redirect, g
import datetime
from rrd.model.portal.top_proc_recorder import TopProcRecorder
import commands
import json
import re

url = "127.0.0.1:3000/lua/get_flows_data.lua?perPage=10"
user = "admin"
psw = "adminadmin"
all_data_type = ["column_duration", "column_server", "column_ndpi", "column_proto_l4", 'column_client', "column_thpt", "column_bytes"]

def remove_html(raw_html):
    cleanr = re.compile("<A.*?>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("</A>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("<div.*?>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("</div>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("<img.*?>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("</img>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("<i.*?>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("</i>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("<span.*?>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("</span>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    raw_html = raw_html.replace("&nbsp;",'')
    return raw_html

def get_forbid_flows():
    cmd = 'iptables-save'
    ip_data = commands.getoutput(cmd)
    if ip_data == '':
        return []
    ip_data = ip_data.split('OUTPUT ACCEPT')[1]
    ip_data = ip_data.split('COMMIT')[0]
    forbidded_flow = ip_data.split('\n')[1:-1]
    for i in range(len(forbidded_flow)):
        curr_row = forbidded_flow[i]
        ip_addr = curr_row.split()[3]
        ip_addr = ip_addr.split('/')[0]
        forbidded_flow[i] = ip_addr
    return forbidded_flow

def get_page_data(url, user, psw, page_num):
    cmd = 'curl -s --cookie "user=%s; password=%s" ' % (user, psw)
    cmd = cmd + '"' + url + '&currentPage=' + str(page_num) +'"'
    flows_data = commands.getoutput(cmd)
    return flows_data

def ipv4_filter(flows_data, ipv4_only):
    if ipv4_only == "false":
        return [flows_data, len(flows_data)]
    else:
        new_flows_data = []
        for data in flows_data:
            if data['column_client'].count('.') == 3:
                if str.isdigit(data['column_client'].split('.')[0].encode('utf-8')) and str.isdigit(data['column_client'].split('.')[1].encode('utf-8')) and str.isdigit(data['column_client'].split('.')[2].encode('utf-8')):
                    new_flows_data.append(data)
        return [new_flows_data, len(new_flows_data)]

def protocol_filter(flows_data, protocol_selection):
    if protocol_selection == 'all':
        return [flows_data, len(flows_data)]
    elif protocol_selection == 'tcp_only':
        new_flows_data = []
        for data in flows_data:
            if data['column_proto_l4'] == 'TCP':
                new_flows_data.append(data)
        return [new_flows_data, len(new_flows_data)]
    else:
        new_flows_data = []
        for data in flows_data:
            if data['column_proto_l4'] == 'UDP':
                new_flows_data.append(data)
        return [new_flows_data, len(new_flows_data)]

def compare_measure(measure1, measure2):
    if measure1 == 'bit/s' and measure2 == 'bit/s':
        return 0
    elif measure1 == 'bit/s' and measure2 in ['kbit/s', 'mbit/s', 'gbit/s']:
        return -1
    elif measure1 == 'kbit/s' and measure2 == 'bit/s':
        return 1
    elif measure1 == 'kbit/s' and measure2 == 'kbit/s':
        return 0
    elif measure1 == 'kbit/s' and measure2 in ['mbit/s', 'gbit/s']:
        return -1
    elif measure1 == 'mbit/s' and measure2 in ['bit/s', 'kbit/s']:
        return 1
    elif measure1 == 'mbit/s' and measure2 == 'mbit/s':
        return 0
    elif measure1 == 'mbit/s' and measure2 == 'gbit/s':
        return -1
    elif measure1 == 'gbit/s' and measure2 in ['bit/s', 'kbit/s', 'mbit/s']:
        return 1
    elif measure1 == 'gbit/s' and measure2 == 'gbit/s':
        return 0
    else:
        return 2

def add_thpt(thpt_1, thpt_2):
    [value1, measure1] = [float(thpt_1.split()[0]), thpt_1.split()[1]]
    [value2, measure2] = [float(thpt_2.split()[0]), thpt_2.split()[1]]
    total = 0
    compare_result = compare_measure(measure1, measure2)
    if compare_result == 2:
        return thpt_1
    elif compare_result == 0:
        total_value = value1 + value2
        total_measure = measure1
    elif compare_result == 1:
        total_value = value1
        total_measure = measure1
    else:
        total_value = value2
        total_measure = measure2
    return str(total_value) + " " + total_measure

def get_data_once(url, user, psw, ipv4_only, protocol_selection, merge_ip_choice, start_page):
    max_page_get = start_page + 4
    require_num = 10
    curr_num = 0
    page_count = start_page - 1
    return_data = []
    
    total_row = 0

    while (curr_num < require_num) and (page_count < max_page_get):
        page_count = page_count + 1
        flows_data = get_page_data(url, user, psw, page_count)
        flows_data = remove_html(flows_data)
        flows_data = '{' + '{'.join(flows_data.split('{')[1:])
        flows_data = unicode(flows_data, errors='ignore')
        flows_data = json.loads(flows_data)
        total_row = flows_data['totalRows']
        [flows_data['data'], curr_num] = ipv4_filter(flows_data['data'], ipv4_only)
        [flows_data['data'], curr_num] = protocol_filter(flows_data['data'], protocol_selection)
        return_data = return_data + flows_data['data']
    
    if merge_ip_choice == 'false':
        return [return_data, total_row]
    else:
        new_return_data = []
        for data in return_data:
            if_stored = False
            for new_data in range(len(new_return_data)):
                if data['column_client'].split(':')[0] == new_return_data[new_data]['column_client']:
                    if_stored = True
                    new_return_data[new_data]["column_bytes"] = str(float(new_return_data[new_data]["column_bytes"].split()[0]) + float(data["column_bytes"].split()[0])) + ' ' + data["column_bytes"].split()[1]
                    if new_return_data[new_data]["column_ndpi"] != data["column_ndpi"]:
                        new_return_data[new_data]["column_ndpi"] = new_return_data[new_data]["column_ndpi"] + '/' + data["column_ndpi"]
                    if new_return_data[new_data]["column_server"] != data["column_server"]:
                        new_return_data[new_data]["column_server"] = new_return_data[new_data]["column_server"] + '/' + data["column_server"]
                    new_return_data[new_data]["column_thpt"] = add_thpt(new_return_data[new_data]["column_thpt"], data["column_thpt"])
            if if_stored == False:
                data['column_client'] = data['column_client'].split(':')[0]
                new_return_data.append(data)
        return [new_return_data, total_row]

@app.route('/portal/flows')
def get_flow_page():
    limit = int(request.args.get("limit") or 10)
    page = int(request.args.get("p") or 1)
    if request.args.get("ipv4_only") == None:
        curr_ipv4_only = 'false'
    else:
        curr_ipv4_only = str(request.args.get("ipv4_only"))
    
    if request.args.get("merge_ip") == None:
        curr_merge_ip = 'false'
    else:
        curr_merge_ip = str(request.args.get("merge_ip"))

    if request.args.get("protocol_choice") == None:
        curr_proc_choice = 'all'
    else:
        curr_proc_choice = str(request.args.get("protocol_choice"))
        
    flows_data = get_page_data(url, user, psw, page)
    flows_data = remove_html(flows_data)
    flows_data = '{' + '{'.join(flows_data.split('{')[1:])
    flows_data = unicode(flows_data, errors='ignore')
    flows_data = json.loads(flows_data)
    total_row = int(flows_data['totalRows'])
    return render_template(
        'portal/flows/index.html', **locals()
    )


@app.route('/api/get_flow')
def get_flows():
    ipv4_only = request.args.get("ipv4_only")
    protocol_selection = request.args.get("protocol_selection")
    merge_ip_choice = request.args.get("if_merge_ip")
    if request.args.get("start_page") == None:
        start_page = 1
    else:
        start_page = int(request.args.get("start_page"))
    ret = {
            "ok": False,
            "data": "",
            "total_row": 0,
            }
    try:
        [flow_data, total_row] = get_data_once(url, user, psw, ipv4_only, protocol_selection, merge_ip_choice, start_page)
        ret["data"] = flow_data
        ret["total_row"] = total_row
        ret['ok'] = True
        return json.dumps(ret)
    except Exception as e:
        abort(400, str(ret))


@app.route('/flow/forbid', methods=["POST",])
def forbid_ip():
    ip_addr = request.form.get("ip_addr")
    ret = { "msg": "", }
    try:
        command = "iptables -I INPUT -s " + ip_addr + " -j DROP"
        commands.getoutput(command)
        command = "iptables-save"
        commands.getoutput(command)
        ret["msg"] = "Finish Forbid"
        return json.dumps(ret)
    except Exception as e:
        ret["msg"] = str(e)
        return json.dumps(ret)

@app.route('/flow/unforbid', methods=["POST",])
def flow_unforbid():
    ip_addr = request.form.get("ip_addr")
    ret = { "msg": "", }
    try:
        command = "iptables -D INPUT -s " + ip_addr + " -j DROP"
        commands.getoutput(command)
        
        command = "iptables-save"
        commands.getoutput(command)
        ret["msg"] = "Finish unforbid"
        return json.dumps(ret)
    except Exception as e:
        ret["msg"] = str(e)
        return json.dumps(ret)

@app.route("/portal/flows/unforbid", methods=["GET", "POST"])
def get_flow_unforbid():
    forbid_ips = get_forbid_flows()
    return render_template("/portal/flows/unforbid.html", **locals())
