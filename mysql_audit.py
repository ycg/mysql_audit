import os, json
from gevent import pywsgi
from flask import Flask, app, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, LoginManager, current_user

import settings
from src import common_util, cache, user_login, sql_manager, host_manager, user_manager

app = Flask("mysql_audit")
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login_home"
login_manager.init_app(app=app)

cache.MyCache().load_all_cache()

#region tab

@app.route("/main")
@login_required
def main():
    return render_template("main.html")

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

#endregion

#region sql audit

@app.route("/audit")
@login_required
def sql_audit():
    return render_template("audit.html", host_infos=sql_manager.get_audit_mysql_host())

@app.route("/audit/check", methods=["POST"])
@login_required
def get_sql_audit_info():
    return sql_manager.audit_sql(get_object_from_json(request.form))

@app.route("/audit/check/<int:id>", methods=["GET", "POST"])
@login_required
def get_sql_audit_info_by_sql_id(id):
    return sql_manager.audit_sql_by_sql_id(id)

@app.route("/audit/db_names/<int:host_id>", methods=["GET", "POST"])
@login_required
def get_database_names(host_id):
    return sql_manager.get_database_names(host_id)

#endregion

#region sql execute

@app.route("/execute")
@login_required
def sql_work():
    return render_template("sql_work_add.html", host_infos=sql_manager.get_execute_mysql_host(), dba_users=cache.MyCache().get_user_info_by_role(settings.ROLE_DBA))

@app.route("/execute/add", methods=["POST"])
@login_required
def add_sql_work():
    return sql_manager.add_sql_work(get_object_from_json(request.form))

@app.route("/execute/delete/<int:id>")
@login_required
def delete_sql_work(id):
    return sql_manager.delete_sql_work(id)

@app.route("/execute/sql/exeucte/<int:id>", methods=["GET", "POST"])
@login_required
def get_sql_execute_home(id):
    return render_template("sql_execute.html", sql_info=sql_manager.get_sql_info_by_id(id))

@app.route("/execute/now/<int:sql_id>", methods=["GET", "POST"])
@login_required
def sql_execute_by_sql_id(sql_id):
    obj = get_object_from_json(request.form)
    obj.sql_id = sql_id
    return render_template("sql_execute_view.html", audit_infos=sql_manager.sql_execute(obj))

@app.route("/execute/result/<int:sql_id>", methods=["GET", "POST"])
@login_required
def get_sql_result(sql_id):
    return sql_manager.get_sql_result(sql_id)

#endregion

#region sql list

@app.route("/list")
@login_required
def sql_list_home():
    return render_template("list.html", user_infos=cache.MyCache().get_user_info(), sql_work_status=settings.SQL_WORK_STATUS_DICT)

@app.route("/list/query", methods=["POST"])
@login_required
def query_sql_list():
    obj = get_object_from_json(request.form)
    return render_template("list_view.html",
                           sql_list=sql_manager.get_sql_list(obj),
                           page_number=obj.page_number,
                           page_list=get_page_number_list(obj.page_number))

@app.route("/list/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_sql_list(id):
    pass

def get_page_number_list(page_number):
    if(page_number <= 5):
        page_list = range(1, 10)
    else:
        page_list = range(page_number - 5, page_number + 6)
    return page_list

#endregion

#region host api

@app.route("/host")
@login_required
def get_host():
    return render_template("host.html")

@app.route("/host/query", methods=["POST"])
@login_required
def query_host():
    return render_template("host_view.html", host_infos=host_manager.query_host_infos(get_object_from_json(request.form)))

@app.route("/host/add", methods=["POST"])
@login_required
def add_host():
    host_manager.add(get_object_from_json(request.form))
    return "add mysql host ok!"

@app.route("/host/update", methods=["POST"])
@login_required
def update_host():
    return "update ok"

@app.route("/host/delete", methods=["POST"])
@login_required
def delete_host():
    host_manager.delete(get_object_from_json(request.form))
    return "delete mysql host ok!"

@app.route("/host/test", methods=["POST"])
@login_required
def test_connection():
    return host_manager.test_connection(get_object_from_json(request.form))

@app.route("/host/query/host_id", methods=["POST"])
@login_required
def get_host_info():
    return host_manager.get_host_info(get_object_from_json(request.form))

#endregion

#region user api

@app.route("/user")
@login_required
def get_user():
    return render_template("user.html", role_infos=cache.MyCache().get_role_info())

@app.route("/user/query", methods=["POST"])
@login_required
def query_user():
    return render_template("user_view.html", user_infos=user_manager.query_user(None))

#endregion

#region login api

@app.route("/login/verfiy", methods=['GET', 'POST'])
def login_verfiy():
    result = common_util.Entity()
    result.error = ""
    result.success = ""
    user_tmp = user_login.User(request.form["userName"])
    if(user_tmp.verify_password(request.form["passWord"], result) == True):
        login_user(user_tmp)
    return json.dumps(result, default=lambda o: o.__dict__)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@login_manager.user_loader
def load_user(user_id):
    return user_login.User(None).get(user_id)

@app.route("/login")
def login_home():
    return "<p hidden>login_error</p>" + render_template("login.html")

#endregion

#region commcon method

def get_object_from_json(json_value):
    obj = common_util.Entity()
    for key, value in dict(json_value).items():
        if(value[0].isdigit()):
            setattr(obj, key, int(value[0]))
        else:
            if(value[0] == "null"):
                setattr(obj, key, None)
            else:
                setattr(obj, key, value[0])
    obj.current_user_id = current_user.id
    return obj

#endregion

#region run server

if __name__ == '__main__':
    port = 5200
    ip = "0.0.0.0"
    if(settings.LINUX_OS):
        print("linux start ok.")
        server = pywsgi.WSGIServer((ip, port), app)
        server.serve_forever()
    if(settings.WINDOWS_OS):
        print("windows start ok.")
        app.run(debug=True, host=ip, port=port, use_reloader=False)

#endregion

