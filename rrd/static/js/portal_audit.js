function start_audit(script_name) {
    document.getElementById("command-security-audit-display").style.display = "block";
    document.getElementById("lynis_details").style.display = "none";
    document.getElementById("lynis_details").style.display = "block";
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
    document.getElementById("lynis_details").style.display = "block";

    get_lynis_details('visual_report');
}



function get_lynis_details(type) {
    document.getElementById("command-security-audit-display").style.display = "block";
    $.getJSON("/api/security/detail_report", {audit_method:'lynis', detail_type: type}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return;
        }
        if (ret.data === "") {
            ret.data = "未执行过lynis"  + "或者仍在运行中。";
        }
        if (type == "report") {
            document.getElementById("command-lynis-visual-report").classList = "command-detail-button pull-left"
            document.getElementById("command-lynis-report").classList = "command-detail-button-clicked pull-left"
            document.getElementById("command-lynis-warning").classList = "command-detail-button pull-left"
            document.getElementById("command-lynis-suggestion").classList = "command-detail-button pull-left"
            document.getElementById("audit-result").innerHTML = ret.data;
            document.getElementById("visual-audit-result").style = "display:none;"
            document.getElementById("audit-result").style = "display:block;"
        } else if (type == "warning"){
            document.getElementById("command-lynis-visual-report").classList = "command-detail-button pull-left"
            document.getElementById("command-lynis-report").classList = "command-detail-button pull-left"
            document.getElementById("command-lynis-warning").classList = "command-detail-button-clicked pull-left"
            document.getElementById("command-lynis-suggestion").classList = "command-detail-button pull-left"
            document.getElementById("audit-result").innerHTML = ret.data;
            document.getElementById("visual-audit-result").style = "display:none;"
            document.getElementById("audit-result").style = "display:block;"
        } else if (type == "suggestion") {
            document.getElementById("command-lynis-visual-report").classList = "command-detail-button pull-left"
            document.getElementById("command-lynis-report").classList = "command-detail-button pull-left"
            document.getElementById("command-lynis-warning").classList = "command-detail-button pull-left"
            document.getElementById("command-lynis-suggestion").classList = "command-detail-button-clicked pull-left"
            document.getElementById("audit-result").innerHTML = ret.data;
            document.getElementById("visual-audit-result").style = "display:none;"
            document.getElementById("audit-result").style = "display:block;"
        } else if (type == 'visual_report') {
            document.getElementById("command-lynis-visual-report").classList = "command-detail-button-clicked pull-left"
            document.getElementById("command-lynis-report").classList = "command-detail-button pull-left"
            document.getElementById("command-lynis-warning").classList = "command-detail-button pull-left"
            document.getElementById("command-lynis-suggestion").classList = "command-detail-button pull-left"
            document.getElementById("visual-audit-result").innerHTML = '<br>' + ret.data;
            document.getElementById("audit-result").style = "display:none;"
            document.getElementById("visual-audit-result").style = "display:block; margin-top:50px;"
        }
        
        // display result
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}