from rrd import app
from flask import render_template, abort, request, url_for, redirect, g
import datetime
from rrd.model.portal.top_proc_recorder import TopProcRecorder

def get_process_info(show_process_num):
    rank = 1
    result = []
    while TopProcRecorder.exists('rank=%s', [rank]):
        curr_row = TopProcRecorder.select_vs(where='rank = %s', params=[rank])[0]
        result.append([curr_row.procname, curr_row.pid, curr_row.user, curr_row.cpu_usage, curr_row.mem_usage, curr_row.datatime])
        rank = rank + 1
    return result

@app.route('/portal/process')
def process_get():

    show_process_num = 6
    data = get_process_info(show_process_num)

    return render_template(
        'portal/process/index.html', **locals()
    )


