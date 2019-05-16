from rrd import app
from flask import render_template, abort, request, url_for, redirect, g
import datetime
from rrd.model.portal.top_proc_recorder import TopProcRecorder
import socket 


@app.route('/ntopng')
def ntopng_redirect():
    host_name = socket.gethostname() 
    host_ip = socket.gethostbyname(host_name) 
    redirect_addr = "http://" + host_ip + ":3000"
    return redirect(redirect_addr)

