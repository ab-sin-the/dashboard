import commands
import json
import re

url = "127.0.0.1:3000/lua/get_flows_data.lua?perPage=10"
user = "admin"
psw = "adminadmin"
all_data_type = ["column_duration", "column_server", "column_ndpi", "column_proto_l4", 'column_client', "column_thpt", "column_bytes"]

def remove_html(raw_html):
    cleanr = re.compile('<.*?>')
    raw_html = re.sub(cleanr, '', raw_html)
    raw_html = re.sub(cleanr, '', raw_html)
    raw_html = re.sub(cleanr, '', raw_html)
    raw_html = raw_html.replace("&nbsp;",'')
    return raw_html

def get_data_once(url, user, psw):
    cmd = 'curl -s --cookie "user=%s; password=%s" ' % (user, psw)
    cmd = cmd + '"' + url + '"'
    flows_data = commands.getoutput(cmd)
    flows_data = remove_html(flows_data)
    flows_data = '{' + '{'.join(flows_data.split('{')[1:])
    print(flows_data)
    flows_data = json.loads(flows_data)
    return flows_data['data']

    
def get_forbid_flows():
    cmd = 'iptables-save'
    ip_data = commands.getoutput(cmd)
    ip_data_lines = ip_data.split('\n')
    forbidded_flow = ip_data_lines[5:-2]
    for i in range(len(forbidded_flow)):
        curr_row = forbidded_flow[i]
        ip_addr = curr_row.split()[3]
        ip_addr = ip_addr.split('/')[0]
        forbidded_flow[i] = ip_addr
    return forbidded_flow

if __name__ == "__main__":
    #all_datas = get_data_once(url, user, psw)
    all_data = get_forbid_flows()