function init_web(url) {
    set_tab_active(url)
    $.get(url, "", function (data) {
        var login_flag = data.substring(0, 25);
        if (login_flag == "<p hidden>login_error</p>") {
            window.location.href = 'login';
        }
        else {
            $("#div_web").html(data);
        }
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

function input_data_for_post_loding(url, json_data, div_id) {
    show_modal_dialog("#loading")
    $.post(url, json_data, function (data) {
        $(div_id).html(data)
        hide_modal_dialog("#loading")
    });
}

function post_request(url, json_data) {
    $.post(url, json_data, function (data) {
        alert(data)
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
        $(this).val(0)
    });
});

function convert_int(id) {
    var value = $(id).val()
    if (value == "") {
        return 0
    }
    return value
}

function convert_string(id) {
    var value = $(id).val()
    if (value.length <= 0) {
        return ""
    }
    return value
}

function get_form_json(frm) {
    var o = {};
    var a = $(frm).serializeArray();
    $.each(a, function () {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
}