function get_flow_data() {
    $.getJSON("/api/get_flow", {ipv4_only: this.if_ipv4_only, protocol_selection: this.protocol_selection, if_merge_ip: this.merge_ip, start_page: this.page_num}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return_val = ""
            return;
        }
        update_table(ret.data, ret.total_row)
       // file_content.html(ret.data)
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}

function forbid_ip(ip_addr, key){
    ip_addr = ip_addr.split(":")[0];
    button_id = "forbid_button_" + key;
    if (ip_addr.split(".").length === 4) {
        $.post('/flow/forbid', {'ip_addr': ip_addr}, function (json) {
            document.getElementById(button_id).innerHTML = "已禁止"
        }, "json");
        return true;
    }
    return false;
}

function create_single_line(data_len) {
    var tableData = "<tr>"

    tableData += "<td>" + data_len["column_ndpi"] + "</td>";
    tableData += "<td>" + data_len["column_proto_l4"] + "</td>";
    tableData += "<td>" + data_len["column_client"] + "</td>";
    tableData += "<td>" + data_len["column_server"] + "</td>";
    tableData += "<td>" + data_len["column_duration"] + "</td>";
    tableData += "<td>" + data_len["column_thpt"] + "</td>";
    tableData += "<td>" + data_len["column_bytes"] + "</td>";
    button_id = "forbid_button_" + data_len["key"];
    tableData += '<td> <span  style="height:26px;background:rgba(255,255,255,1);border-radius:5px;border:1px solid rgba(242,242,242,1);cursor: pointer; font-size:10px;font-family:PingFangSC-Semibold;font-weight:600;color:rgba(221,77,84,1);padding: 6px 15px" onclick="forbid_ip(' + "'" + data_len["column_client"] + "'" + "," + data_len["key"]  + ')";  id="' + button_id + '" >  禁止访问 ' +  "</span></td>";
    tableData += "</tr>"
    return tableData;
}

function update_table(data, total_row) {
    var row_len = data.length;
    var table_whole = ""
    for(var i = 0; i < row_len; i++){
        table_whole += create_single_line(data[i])
    }
    $("#flow_table").html(table_whole);
}

var update_flow = setInterval(get_flow_data, 5000);
var url = window.location.search;
var page_num = get_query_val('p')
if (page_num === null) {
    page_num = 1;
}

var merge_ip = get_query_val('merge_ip')
var if_ipv4_only = get_query_val('ipv4_only')
var protocol_selection = get_query_val('protocol_choice')
if (merge_ip === null) {
    merge_ip = 'false';
}
if (if_ipv4_only === null) {
    if_ipv4_only = 'false';
}
if (protocol_selection === null) {
    protocol_selection = 'all';
}



function change_auto_refresh(auto_refresh) {
    if (auto_refresh.checked == true) {
        this.update_flow = setInterval(get_flow_data, 5000);
    }
    if (auto_refresh.checked == false) {
        clearInterval(this.update_flow);
    }
}

function change_ipv4_show_case() {
    if (this.if_ipv4_only == 'true') {
        this.if_ipv4_only = false;
        replace_query_val('ipv4_only', false)
    } else {
        this.if_ipv4_only = true;
        replace_query_val('ipv4_only', true)
    }
    get_flow_data();
}

function change_merge_ip_choice() {
    if (this.merge_ip == 'true') {
        this.merge_ip = false;
        replace_query_val('merge_ip', false);
    }else {
        this.merge_ip = true;
        replace_query_val('merge_ip', true);
    }
    get_flow_data();
}

function change_protocol_selection(select_choice) {
    this.protocol_selection = select_choice;
    replace_query_val('protocol_choice', select_choice);
    get_flow_data();
}


function get_query_val(query_name){
    var reg_expr = new RegExp("(^|&)" + query_name + "=([^&]*)(&|$)");
    var res = window.location.search.substr(1).match(reg_expr);
    if (res != null) {
        return unescape(res[2]);
    } else {
        return null;
    }
}

function replace_query_val(query_name, new_val){
    if (get_query_val(query_name) !== null) {
        var old_url = this.location.href.toString();
        var reg_expr = eval('/(' + query_name + '=)([^&]*)/gi');
        var new_url = old_url.replace(reg_expr, query_name + '=' + new_val); 
        this.location = new_url;
        window.location.href = new_url;
    } else {
        var old_url = this.location.href.toString();
        if (old_url.substr(-5) === 'flows') {
            var new_url = old_url + '?&' + query_name + '=' + new_val;
        } else {
            var new_url = old_url + '&' + query_name + '=' + new_val;
        }
        this.location = new_url;
        window.location.href = new_url;
    }
}


window.onload = () => {
    get_flow_data();
    var change_merge_choice_button_id = "merge_ip_choice_button";
    var change_ipv4_button_id = "ipv4_only_button";
    var protocol_selection_id = "protocol_selection"


    if (this.merge_ip == 'false' ) {
        document.getElementById(change_merge_choice_button_id).innerHTML = "同IP多端口合并"
    } else {
        document.getElementById(change_merge_choice_button_id).innerHTML = "不合并相同IP"
    }

    if (this.if_ipv4_only == 'false') {
        document.getElementById(change_ipv4_button_id).innerHTML = "仅显示IPv4"
    } else {
        document.getElementById(change_ipv4_button_id).innerHTML = "显示所有IP"
    }

    if (this.protocol_selection ==  'all') {
        document.getElementById(protocol_selection_id)[0].selected = true;
    } else if (this.protocol_selection == 'tcp_only') {
        document.getElementById(protocol_selection_id)[1].selected = true;
    } else {
        document.getElementById(protocol_selection_id)[2].selected = true;
    }
}
