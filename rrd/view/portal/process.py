from rrd import app
from flask import render_template, abort, request, url_for, redirect, g
import os
import datetime

def get_process_info(show_process_num):
    active_proc = os.popen('top -bi -n 1 -d 0.1').read().encode().decode().split('\n\n')[1].split('\n')
    active_proc_header = active_proc[0]
    active_proc_list = active_proc[1:-1]
    active_proc_num = len(active_proc_list)
    result = []
    for single_proc in active_proc_list:
        single_proc_prop = single_proc.split()
        Pid = single_proc_prop[0]
        User = single_proc_prop[1]
        cpu_usage = single_proc_prop[8]
        mem_usage = single_proc_prop[9]
        name = single_proc_prop[11]
        result.append([name, Pid, User, cpu_usage + "%", mem_usage + "%", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    if len(result) > show_process_num:
        result = result[:6]
    return result

@app.route('/portal/process')
def process_get():

    show_process_num = 6
    data = get_process_info(show_process_num)

    return render_template(
        'portal/process/index.html', **locals()
    )


