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
from rrd import config
from flask import render_template, abort, request, url_for, redirect, g
from rrd.model.portal.host_group import HostGroup
from rrd.model.screen import DashboardScreen
from rrd.model.graph import DashboardGraph
from rrd.utils.logger import logging
from rrd.utils.graph_urls import generate_graph_urls 
import json
from welcome_graph import *
log = logging.getLogger(__file__)
default_screen_name = "DefaultScreen"

'''
@app.route('/portal/home', methods=["GET",])
def welcome_page_get():
    start = request.args.get("start")
    end = request.args.get("end")
    all_graphs = []
    screen = True
    for graph in graphs:
        log.debug("fawfw")
        graph_class = DashboardGraph(0, graph["title"], graph["endpoints"], graph["counters"], \
        graph["screen_id"], graph["timespan"], graph["graph_type"])
        
        all_graphs.extend(generate_graph_urls(graph_class, start, end)) or []
    return render_template("index.html", **locals())
'''

@app.route('/portal/home', methods=["GET",])
def welcome_page_get():
    start = request.args.get("start")
    end = request.args.get("end")
    screens = DashboardScreen.gets_all()
    default_screen = None
    for screen in screens:
        if screen.name == default_screen_name:
            default_screen = screen

    if not default_screen:
        abort(404, "Default Screen not Created.")

    pid = default_screen.id

    sub_screens = DashboardScreen.gets_by_pid(pid = pid) 

    default_sub_screen = sub_screens[0]
    for sub_screen in sub_screens:
        if sub_screen.name == "ALL":
            default_sub_screen = sub_screen

    graphs = DashboardGraph.gets_by_screen_id(default_sub_screen.id)
    all_graphs = []

    for graph in graphs:
        all_graphs.extend(generate_graph_urls(graph, start, end)) or []
    
    all_graphs = sorted(all_graphs, key=lambda x: (x.position, x.id))

    return render_template("index.html", **locals())
