from gevent import pywsgi
from flask import Flask, app, render_template, request

import settings
from control import host
from common import inception_util, entity, cache

app = Flask(__name__)

cache.MyCache().load_all_cache()

#region tab

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/audit")
def sql_audit():
    return render_template("audit.html")

@app.route("/execute")
def sql_execute():
    return render_template("execute.html")

@app.route("/list")
def sql_list():
    return render_template("list.html")

#endregion

#region sql audit

@app.route("/audit/check", methods=["POST"])
def get_sql_audit_info():
    return render_template("audit_view.html", audit_infos=inception_util.sql_audit(get_object_from_json(request.form).sql, settings.MySQL_HOST))

#endregion

#region host api

@app.route("/host")
def get_host():
    return render_template("host.html")

@app.route("/host/query", methods=["POST"])
def query_host():
    return render_template("host_view.html", host_infos=host.query_host_infos(get_object_from_json(request.form)))

@app.route("/host/add", methods=["POST"])
def add_host():
    host.add(get_object_from_json(request.form))
    return "add mysql host ok!"

@app.route("/host/update", methods=["POST"])
def update_host():
    return "update ok"

@app.route("/host/delete", methods=["POST"])
def delete_host():
    host.delete(get_object_from_json(request.form))
    return "delete mysql host ok!"

@app.route("/host/test", methods=["POST"])
def test_connection():
    return host.test_connection(get_object_from_json(request.form))

@app.route("/host/query/host_id", methods=["POST"])
def get_host_info():
    return host.get_host_info(get_object_from_json(request.form))

#endregion

#region user api

@app.route("/user")
def get_user():
    return render_template("user.html")

#endregion

#region commcon method

def get_object_from_json(json_value):
    obj = entity.Entity()
    for key, value in dict(json_value).items():
        if(value[0].isdigit()):
            setattr(obj, key, int(value[0]))
        else:
            setattr(obj, key, value[0])
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

