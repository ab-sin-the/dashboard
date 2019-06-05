function unforbid_ip(ele){
    ip_to_unforbided = $(ele).parent().siblings(":first").text();
    ip_to_unforbided = ip_to_unforbided.replace(/\s+/g, '');
    $(ele)[0].innerHTML = "已允许"
    $.post('/flow/unforbid', {'ip_addr': ip_to_unforbided}, function (json) {
        $(ele).innerHTML = "已允许"
    }, "json");
}