function fn_search_log_file() {
    var input_command = $.trim($("input[name='execute_command']").val());
    var button = document.getElementById('refresh_button');
    $.getJSON("/api/execute_command", {command:input_command}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return;
        }

        // display log
        document.getElementById("command_result").innerText = ret.data;
        button.style.visibility = 'visible';
       // file_content.html(ret.data)
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}

function refresh_log() {
    var file_path = $("#execute-command").val();
    var button = document.getElementById('refresh_button');
    $.getJSON("/api/execute_command", {command:input_command}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return;
        }

        // display log
        document.getElementById("command_result").innerText = ret.data;
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}