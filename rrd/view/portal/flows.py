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
    cleanr = re.compile("<A.*?</A>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("<div.*?</div>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("</div>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("<img.*?</img>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("<i.*?</i>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    raw_html = raw_html.replace("&nbsp;",'')
    return raw_html

def get_forbid_flows():
    cmd = 'iptables-save'
    ip_data = commands.getoutput(cmd)
    ip_data = ip_data.split('OUTPUT ACCEPT')[1]
    ip_data = ip_data.split('COMMIT')[0]
    forbidded_flow = ip_data.split('\n')[1:-1]
    for i in range(len(forbidded_flow)):
        curr_row = forbidded_flow[i]
        ip_addr = curr_row.split()[3]
        ip_addr = ip_addr.split('/')[0]
        forbidded_flow[i] = ip_addr
    return forbidded_flow

def get_data_once(url, user, psw):
    cmd = 'curl -s --cookie "user=%s; password=%s" ' % (user, psw)
    cmd = cmd + '"' + url + '"'
    flows_data = commands.getoutput(cmd)
    flows_data = remove_html(flows_data)
    flows_data = '{' + '{'.join(flows_data.split('{')[1:])
    flows_data = json.loads(flows_data)
    return flows_data['data']

@app.route('/portal/flows')
def get_flow_page():
    return render_template(
        'portal/flows/index.html', **locals()
    )


@app.route('/api/get_flow')
def get_flows():
    ret = {
            "ok": False,
            "data": "",
            }
    try:
        flow_data = get_data_once(url, user, psw)
        ret["data"] = flow_data
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
    print("aaa")
    ip_addr = request.form.get("ip_addr")
    ret = { "msg": "", }
    try:
        command = "iptables -D INPUT -s " + ip_addr + " -j DROP"
        print(command)
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
