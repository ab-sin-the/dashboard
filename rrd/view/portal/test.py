


import re








aa = '{"data":[{"column_duration":"< 1 sec","column_vlan":0,"column_bytes":"3.12 KB","column_info":"sourest.net/chart/a?id=5...","column_proto_l4":"TCP","column_server":"<A HREF=\'/lua/host_details.lua?host=172.19.233.84\' data-toggle=\'tooltip\' title=\'sourest.net&#10;nw latency: 0.009 ms\' >sourest.net&nbsp;<i class=\'fa fa-flag\'></i></A>:<A HREF=\'/lua/port_details.lua?port=8081\'>tproxy</A> ","column_client":"<A HREF=\'/lua/host_details.lua?host=59.78.171.149\' data-toggle=\'tooltip\' title=\'59.78.171.149&#10;nw latency: 34.007 ms\' >59.78.171.149</A> <A HREF=\'/lua/hosts_stats.lua?country=CN\'><img src=\'/img/blank.gif\' class=\'flag flag-cn\'></A> :<A HREF=\'/lua/port_details.lua?port=49464\'>49464</A> ","column_ndpi":"<A HREF=\'/lua/hosts_stats.lua?protocol=7\'> HTTP <i class=\'fa fa-thumbs-o-up\' alt=\'Acceptable Protocol\'></i></A>","key":3882049231,"column_key":"<A HREF=\'/lua/flow_details.lua?flow_key=3882049231\'><span class=\'label label-info\'>Info</span></A>","column_breakdown":"<div class=\'progress\'><div class=\'progress-bar progress-bar-warning\' style=\'width: 29%;\'>Client</div><div class=\'progress-bar progress-bar-info\' style=\'width: 71%;\'>Server</div></div>","column_thpt":"0 bit/s "}],"perPage":10,"sort":[["column_","desc"]],"totalRows":17,"currentPage":1}'



def remove_html(raw_html):
    cleanr = re.compile("<A.*</A>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("<div.*</div>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("<img.*</img>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    cleanr = re.compile("<i.*</i>",re.S)
    raw_html = re.sub(cleanr, '', raw_html)
    raw_html = raw_html.replace("&nbsp;",'')
    return raw_html

print(remove_html(aa))