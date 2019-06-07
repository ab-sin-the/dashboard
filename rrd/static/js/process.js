window.onload = start_update_process;

function start_update_process() {
    get_process_data();
    setInterval(get_process_data, 10000);
}



function get_process_data() {
    $.getJSON("/api/get_process", {}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return_val = ""
            return;
        }
        update_table(ret.data)
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}

function update_table(data) {
    var row_len = data.length;
    var table_whole = ""
    for(var i = 0; i < row_len; i++){
        table_whole += create_single_line(data[i])
    }
    $("#process_table").html(table_whole);
}

function create_single_line(data_len) {
    var tableData = "<tr>"
    tableData += "<td>" + data_len[0] + "</td>";
    tableData += "<td>" + data_len[1] + "</td>";
    tableData += "<td>" + data_len[2] + "</td>";
    tableData += "<td>" + data_len[3] + "</td>";
    tableData += "<td>" + data_len[4] + "</td>";
    tableData += "<td>" + data_len[5] + "</td>";
    tableData += "</tr>"
    return tableData;
}