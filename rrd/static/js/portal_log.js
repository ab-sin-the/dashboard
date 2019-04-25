function fn_search_log_file() {
    var file_path = $.trim($("input[name='logfile_search']").val());

    $.getJSON("/api/log_file", {file:file_path}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return;
        }

        // display_endpoints
        var file_content = $("#log-file-content");
        file_content.html(ret.data)
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}