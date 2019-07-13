function get_query_val(query_name){
    var reg_expr = new RegExp("(^|&)" + query_name + "=([^&]*)(&|$)");
    var res = window.location.search.substr(1).match(reg_expr);
    if (res != null) {
        return unescape(res[2]);
    } else {
        return null;
    }
}

function button_display() {
    var graphs_choice = get_query_val('graphs');
    var all_button_id = 'homepage_button_all';
    var cml_button_id = 'homepage_button_cml';
    var disk_button_id = 'homepage_button_disk';
    var net_button_id = 'homepage_button_net';

    document.getElementById(all_button_id).classList = 'homepage-top-link-button';
    document.getElementById(cml_button_id).classList = 'homepage-top-link-button';
    document.getElementById(disk_button_id).classList = 'homepage-top-link-button';
    document.getElementById(net_button_id).classList = 'homepage-top-link-button';

    if (graphs_choice == null) {
        graphs_choice = 'all';
    }

    console.log(graphs_choice == 'all')
    console.log(graphs_choice == 'cml')
    console.log(graphs_choice == 'disk')
    console.log(graphs_choice == 'net')
    if (graphs_choice == 'all') {
        document.getElementById(all_button_id).classList = 'button-blue-small';
        document.getElementById(all_button_id).style = 'margin-left:0px;'
    } else if (graphs_choice == 'cml') {
        document.getElementById(cml_button_id).classList = 'button-blue-small';
        document.getElementById(all_button_id).style = 'margin-left:20px;'
    } else if (graphs_choice == 'disk') {
        document.getElementById(disk_button_id).classList = 'button-blue-small';
        document.getElementById(all_button_id).style = 'margin-left:20px;'
    } else if (graphs_choice == 'net') {
        document.getElementById(net_button_id).classList = 'button-blue-small';
        document.getElementById(all_button_id).style = 'margin-left:20px;'
    }
}

window.onload = button_display;