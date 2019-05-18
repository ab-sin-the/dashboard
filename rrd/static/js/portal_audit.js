function start_audit(script_name) {
    document.getElementById("audit-result").innerText = "正在执行" + script_name + ",请稍等几分钟。";
    $.getJSON("/api/security_audit", {audit_method:script_name}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return;
        }
        if (ret.data === "is running") {
            document.getElementById("audit-result").innerText = script_name + "已经在运行了。";
        }
        // display result
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })

}


function get_report(script_name){
    $.getJSON("/api/security_report", {audit_method:script_name}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return;
        }
        if (ret.data === "") {
            ret.data = "未执行过" + script_name  + "或者仍在运行中。";
        }
        document.getElementById("audit-result").innerText = ret.data;
        // display result
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}