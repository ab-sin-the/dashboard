function get_flow_data() {
    $.getJSON("/api/get_flow", {ipv4_only: this.if_ipv4_only}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return_val = ""
            return;
        }
        update_table(ret.data)
       // file_content.html(ret.data)
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}

function forbid_ip(ip_addr, key){
    ip_addr = ip_addr.split(":")[0];
    button_id = "forbid_button_" + key;
    if (ip_addr.split(".").length == 4) {
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
    tableData += '<td> <button id="' + button_id + '" clsss="btn btn-warning btn-sm" onclick="forbid_ip(' + "'" + data_len["column_client"] + "'" + "," + data_len["key"]  + ')"; > 禁止访问' +  "</button></td>";
    tableData += "</tr>"
    return tableData;
}

function update_table(data) {
    var row_len = data.length;
    var table_whole = ""
    for(var i = 0; i < row_len; i++){
        table_whole += create_single_line(data[i])
    }
    $("#flow_table").html(table_whole);
}

var update_flow = setInterval(get_flow_data, 5000);
var if_ipv4_only = false;

function change_auto_refresh(auto_refresh) {
    if (auto_refresh.checked === true) {
        this.update_flow = setInterval(get_flow_data, 5000);
    }
    if (auto_refresh.checked === false) {
        clearInterval(this.update_flow);
    }
}

function change_ipv4_show_case() {
    var change_ipv4_button_id = "ipv4_only_button";
    if (this.if_ipv4_only === true) {
        this.if_ipv4_only = false;
        document.getElementById(change_ipv4_button_id).innerHTML = "仅显示IPv4"
    } else{
        this.if_ipv4_only = true;
        document.getElementById(change_ipv4_button_id).innerHTML = "显示所有IP"
    }
    get_flow_data();
}


window.onload = get_flow_data;