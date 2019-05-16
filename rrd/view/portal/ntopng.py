from rrd import app
from flask import render_template, abort, request, url_for, redirect, g
import datetime
from rrd.model.portal.top_proc_recorder import TopProcRecorder


@app.route('/ntopng')
def ntopng_redirect():

    return redirect("http://127.0.0.1:3000")

