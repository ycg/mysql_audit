from gevent import pywsgi
from flask import Flask, app, render_template

import settings

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("home.html")

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

