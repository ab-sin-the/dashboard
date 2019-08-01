function start_audit(script_name) {
    document.getElementById("command-security-audit-display").style.display = "block";
    document.getElementById("GScan_details").style.display = "none";
    document.getElementById("GScan_details").style.display = "block";
    document.getElementById("audit-result").innerHTML = "正在执行" + script_name + ",请稍等几分钟。";
    $.getJSON("/api/security_audit", {audit_method:script_name}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return;
        }

        if (ret.data === "is running") {
            document.getElementById("audit-result").innerHTML = script_name + "已经在运行了。";
        }
        // display result
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })


}


function get_report(script_name){
    document.getElementById("command-security-audit-display").style.display = "block";
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
        
        document.getElementById("GScan_details").style.display = "block";
        // display result
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}



function get_Gscan_details(type) {
    document.getElementById("command-security-audit-display").style.display = "block";
    $.getJSON("/api/security/detail_report", {audit_method:'GScan', detail_type: type}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return;
        }
        if (ret.data === "") {
            ret.data = "未执行过GScan"  + "或者仍在运行中。";
        }
        if (type == "report") {
            document.getElementById("command-GScan-report").classList = "command-detail-button-clicked pull-left"
            document.getElementById("command-GScan-all").classList = "command-detail-button pull-left"
            document.getElementById("command-GScan-entry-info").classList = "command-detail-button pull-left"
            document.getElementById("command-GScan-vulun-poss").classList = "command-detail-button pull-left"
        } else if (type == "all") {
            document.getElementById("command-GScan-report").classList = "command-detail-button pull-left"
            document.getElementById("command-GScan-all").classList = "command-detail-button-clicked pull-left"
            document.getElementById("command-GScan-entry-info").classList = "command-detail-button pull-left"
            document.getElementById("command-GScan-vulun-poss").classList = "command-detail-button pull-left"
        } else if (type == "entry_info") {
            document.getElementById("command-GScan-report").classList = "command-detail-button pull-left"
            document.getElementById("command-GScan-all").classList = "command-detail-button pull-left"
            document.getElementById("command-GScan-entry-info").classList = "command-detail-button-clicked pull-left"
            document.getElementById("command-GScan-vulun-poss").classList = "command-detail-button pull-left"
        } else if (type == "vulun_poss") {
            document.getElementById("command-GScan-report").classList = "command-detail-button pull-left"
            document.getElementById("command-GScan-all").classList = "command-detail-button pull-left"
            document.getElementById("command-GScan-entry-info").classList = "command-detail-button pull-left"
            document.getElementById("command-GScan-vulun-poss").classList = "command-detail-button-clicked pull-left"
        }
        document.getElementById("audit-result").innerText = ret.data;
        
        // display result
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}
