from gevent import pywsgi
from flask import Flask, app, render_template, request

import settings
from common import inception_util, entity

app = Flask(__name__)

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

#region sql audit

@app.route("/audit/check", methods=["POST"])
def get_sql_audit_info():
    return render_template("audit_view.html", audit_infos=inception_util.sql_audit(get_object_from_json(request.form).sql, settings.host_info))

#endregion

def get_object_from_json(json_value):
    obj = entity.Entity()
    for key, value in dict(json_value).items():
        if(value[0].isdigit()):
            setattr(obj, key, int(value[0]))
        else:
            setattr(obj, key, value[0])
    return obj

if __name__ == '__main__':
    port = 5200
    host = "0.0.0.0"
    if(settings.LINUX_OS):
        print("linux start ok.")
        server = pywsgi.WSGIServer((host, port), app)
        server.serve_forever()
    if(settings.WINDOWS_OS):
        print("windows start ok.")
        app.run(debug=True, host=host, port=port, use_reloader=False)

