function init_web(url) {
    set_tab_active(url)
    $.get(url, "", function (data) {
        $("#div_web").html(data);
    });
}

function get_data(url) {
    var result_data = "";
    $.get(url, "", function (data) {
        result_data = data;
    });
    return result_data;
}

function post_data(url, input_data) {
    $.post(url, {"keys": input_data}, function (data) {
        return data
    });
}

function show_modal_dialog(id_name) {
    $(id_name).modal("show")
}

function hide_modal_dialog(id_name) {
    $(id_name).modal("hide")
}

function set_tab_active(id_name) {
    if (id_name.length <= 0) {
        return false
    }
    $("#myTab").find("a").each(function () {
        if ($(this).attr("id") == id_name) {
            $(this).addClass("active");
        } else {
            $(this).removeClass("active");
        }
    });
}
