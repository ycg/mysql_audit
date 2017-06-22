function init_web(url) {
    set_tab_active(url)
    $.get(url, "", function (data) {
        $("#div_web").html(data);
    });
}

function input_data_for_get(url, div_id) {
    $.get(url, "", function (data) {
        $(div_id).html(data)
    });
}

function input_data_for_post(url, json_data, div_id) {
    $.post(url, json_data, function (data) {
        $(div_id).html(data)
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

$("button[type='reset']").click(function () {
    $('input').attr("value", '');
    $("textarea").val("");
    $("select.selectpicker").each(function () {
        $(this).selectpicker('val', $(this).find('option:first').val());
        $(this).find("option").attr("selected", false);
        $(this).find("option:first").attr("selected", true);
    });
});