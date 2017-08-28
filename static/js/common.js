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
        hide_modal_dialog("#loading");
    }).error(function () {
        hide_modal_dialog("#loading");
    });
}

function input_data_for_dialog(url, json_data, dialog_name) {
    $.post(url, json_data, function (data) {
        hide_modal_dialog(dialog_name);
    }).error(function () {
        hide_modal_dialog(dialog_name);
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

function get_audit_infos() {
    var sql = $("#sql_value").val();
    var host_id = $("#host_id").val();
    if (host_id <= 0) {
        $("#audit_info").html("请选择数据库集群");
        return;
    }
    else if (jQuery.trim(sql).length <= 0) {
        $("#audit_info").html("请输入要审核的SQL");
        return;
    }
    else if ($("#db_name").val() == null) {
        $("#audit_info").html("请选择要执行的数据库");
        return;
    }
    else {
        var json_obj = new Object();
        json_obj.sql = $("#sql_value").val();
        json_obj.host_id = $("#host_id").val();
        json_obj.db_name = $("#db_name").val();
        input_data_for_post_loding("/audit/check", JSON.stringify(json_obj), "#audit_info");
    }
}

function logout() {
    if (window.confirm("是否确认退出?")) {
        $.post("/logout", "", function (data) {
            alert("logout ok!");
            window.location.href = 'login';
        });
    }
}

