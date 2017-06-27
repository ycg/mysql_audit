import os, json
from gevent import pywsgi
from flask import Flask, app, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, LoginManager, current_user

import settings
from common import entity, cache
from control import host, audit, execute, user_login, sql_list

app = Flask(__name__)
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
    return render_template("audit.html", host_infos=audit.get_audit_mysql_host())

@app.route("/audit/check", methods=["POST"])
@login_required
def get_sql_audit_info():
    return audit.audit_sql(get_object_from_json(request.form))

#endregion

#region sql execute

@app.route("/execute")
@login_required
def sql_work():
    return render_template("execute.html", host_infos=execute.get_execute_mysql_host())

@app.route("/execute/add", methods=["POST"])
@login_required
def add_sql_work():
    execute.add_sql_work(get_object_from_json(request.form))
    return "add ok."

@app.route("/execute/delete/<int:id>")
@login_required
def delete_sql_work(id):
    return execute.delete_sql_work(id)

#endregion

#region sql list

@app.route("/list")
@login_required
def sql_list_home():
    return render_template("list.html")

@app.route("/list/query", methods=["POST"])
@login_required
def query_sql_list():
    print(request.form)
    return render_template("list_view.html", sql_list=sql_list.get_sql_list(get_object_from_json(request.form)))

@app.route("/list/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_sql_list(id):
    pass

#endregion

#region host api

@app.route("/host")
@login_required
def get_host():
    return render_template("host.html")

@app.route("/host/query", methods=["POST"])
@login_required
def query_host():
    return render_template("host_view.html", host_infos=host.query_host_infos(get_object_from_json(request.form)))

@app.route("/host/add", methods=["POST"])
@login_required
def add_host():
    host.add(get_object_from_json(request.form))
    return "add mysql host ok!"

@app.route("/host/update", methods=["POST"])
@login_required
def update_host():
    return "update ok"

@app.route("/host/delete", methods=["POST"])
@login_required
def delete_host():
    host.delete(get_object_from_json(request.form))
    return "delete mysql host ok!"

@app.route("/host/test", methods=["POST"])
@login_required
def test_connection():
    return host.test_connection(get_object_from_json(request.form))

@app.route("/host/query/host_id", methods=["POST"])
@login_required
def get_host_info():
    return host.get_host_info(get_object_from_json(request.form))

#endregion

#region user api

@app.route("/user")
@login_required
def get_user():
    return render_template("user.html")

#endregion

#region login api

@app.route("/login/verfiy", methods=['GET', 'POST'])
def login_verfiy():
    result = entity.Entity()
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
    obj = entity.Entity()
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

