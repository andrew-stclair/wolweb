"""Wake on Lan Webserver written in Python3"""
import os
import platform
import json
import flask

SETTINGS_FILE = "settings.json"
app = flask.Flask(__name__)

# Create a template settings file if one does not exist
if not os.path.exists(SETTINGS_FILE):
    data = {}
    data['devices'] = {}
    data['devices']['localhost'] = {"ip": "127.0.0.1", "mac": "ff:ff:ff:ff:ff:ff"}
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as newfile:
        json.dump(data, newfile, indent=2)

@app.route("/", methods = ['GET'])
def index():
    """Webserver index"""
    result = ""
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as file:
        config = json.load(file)
        result += "<center><table style='padding:10px;'>"
        for device in config['devices'].keys():
            result += f"<tr style='padding:10px;'><td rowspan='2' style='padding:10px;'>{device}</td><td style='text-align: right;'>IP:</td><td>{config['devices'][device]['ip']}</td></tr><tr><td style='text-align: right;'>MAC:</td><td>{config['devices'][device]['mac']}</td></tr>"
        result += "</table></center>"
    result += f"<footer style='position:absolute;width:100%;bottom:10px;color:#BBB;'><center>Host: {platform.node()}</center></footer>"
    resp = flask.Response(result)
    resp.headers['Content-Type'] = "text/html; charset=UTF-8"
    return resp

@app.route("/device/<name>", methods = ['GET', 'POST', 'DELETE'])
def update(name):
    """Do magic with the settings file"""
    if flask.request.method == 'GET':
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as file:
            config = json.load(file)
            resp = flask.Response(json.dumps(config['devices'][name]))
            resp.headers['Content-Type'] = "text/plain; charset=UTF-8"
            return resp
    elif flask.request.method == 'POST':
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as infile:
            config = json.load(infile)
        config['devices'][name] = {"ip": flask.request.form['ip'], "mac": flask.request.form['mac']}
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as outfile:
            json.dump(config, outfile, indent=2)
        resp = flask.Response(json.dumps(config))
        resp.headers['Content-Type'] = "text/plain; charset=UTF-8"
        return resp
    elif flask.request.method == 'DELETE':
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as infile:
            config = json.load(infile)
        obj = config['devices'].pop(name, None)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as outfile:
            json.dump(config, outfile, indent=2)
        resp = flask.Response(json.dumps(obj))
        resp.headers['Content-Type'] = "text/plain; charset=UTF-8"
        return resp

@app.route(f"/{SETTINGS_FILE}", methods = ['GET'])
def settings():
    """Return the settings file"""
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as file:
        resp = flask.Response(file.read())
        resp.headers['Content-Type'] = "text/plain; charset=UTF-8"
        return resp
