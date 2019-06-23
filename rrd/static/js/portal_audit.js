function start_audit(script_name) {
    document.getElementById("lynis_details").style.display = "none";
    document.getElementById("GScan_details").style.display = "none";
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
    if (script_name === "GScan") {
        document.getElementById("lynis_details").style.display = "none";
    } else{
        document.getElementById("GScan_details").style.display = "none";
    }
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
        
        if (script_name === "GScan") {
            document.getElementById("GScan_details").style.display = "block";
        } else{
            document.getElementById("lynis_details").style.display = "block";
        }
        // display result
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}



function get_Gscan_details(type) {
    $.getJSON("/api/security/detail_report", {audit_method:'GScan', detail_type: type}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return;
        }
        if (ret.data === "") {
            ret.data = "未执行过GScan"  + "或者仍在运行中。";
        }
        document.getElementById("audit-result").innerText = ret.data;
        
        // display result
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}

function get_lynis_details(type) {
    $.getJSON("/api/security/detail_report", {audit_method:'lynis', detail_type: type}, function(ret){
        $(".loading").hide();
        if (!ret.ok) {
            err_message_quietly(ret.msg);
            return;
        }
        if (ret.data === "") {
            ret.data = "未执行过lynis"  + "或者仍在运行中。";
        }
        document.getElementById("audit-result").innerText = ret.data;
        
        // display result
    }).error(function(req, ret, errorThrown){
        $(".loading").hide();
        err_message_quietly(req.statusText)
    })
}