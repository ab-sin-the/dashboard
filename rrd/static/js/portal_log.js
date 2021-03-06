function fn_search_log_file() {
    var file_path = $.trim($("input[name='logfile_search']").val());
    var button = document.getElementById('refresh_button');
    $.getJSON("/api/log_file", {file:file_path}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return;
        }

        // display log
        document.getElementById("log-file-content").innerText = ret.data;
        button.style.visibility = 'visible';
       // file_content.html(ret.data)
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}

function refresh_log() {
    var file_path = $("#logfile-search").val();
    var button = document.getElementById('refresh_button');
    $.getJSON("/api/log_file", {file:file_path}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return;
        }

        // display log
        document.getElementById("log-file-content").innerText = ret.data;
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}