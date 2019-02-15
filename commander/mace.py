import sys
import os
import requests
import datetime


def new_task(args):
    '''Create a new task and run it on the given hosts
    Args:
        args (str): the arguments that are passed into the program
            Example (single command):
                t: 8.8.8.8 8.8.8.8 8.8.8.8: echo hi
            Example (script):
                ts: 8.8.8.8 8.8.8.8 8.8.8.8: echo hi
    '''
    try:
        _, ips, command = args.split(":", 2)
        if args.startswith("th:"):
            with open(ips) as ipf:
                hs = ipf.readlines()
        else: 
            hosts = ips.replace(",","").strip().split()
        command = command.strip()
        if not hosts or not command:
            raise Exception("Invalid hosts or commands")
        print("Host(s): " + str(hosts))
        # If its a script, read the script and the command
        if args.startswith("ts:"):
            with open(command) as fil:
                cmd = fil.read()
            print("Script: " + command)
        else:
            # just use the actual command
            cmd = command
            print("Command: " + command)
        

        data = {"hosts": "|".join(hosts), "commands": cmd}
        request = requests.post(server + "/api/commander/push", json=data)
        if request.status_code != 200:
            print("{}:\n{}".format(request.status_code, request.content))
    except Exception as E:
        print(E)
        print("Usage: 't: host[ hosts...]: commands'")

def show_recent(minutes=10):
    '''Given the content of the callback log, parse the hosts and types of callbacks with in the past X minutes
    Args:
        minutes (int, default=10): the number of minutes to show
    Returns:
        dict: A dictionary of the hosts and callback types
            Example:
            {
                '8.8.8.8': set('bash', 'go'),
                '4.4.4.4': set('go', 'bashrc')
            }
    '''
    content = show_calls()
    data = {}
    for line in reversed(content.split("\n")):
        line = line.strip()
        # Skip empty lines
        if not line:
            continue
        # Get the data from the logfile
        date, time, ip, source = line.strip().split()
        # Find the time delta
        log_time = datetime.datetime.strptime(date +" "+time, '%Y-%m-%d %H:%M:%S')
        diff = datetime.datetime.now() - log_time
        # If the logs are older than the time difference, stop parsing
        if diff.seconds > 60*minutes:
            break
        # Add the IP to the data if its not there
        if ip not in data:
            data[ip] = set()
        # Add the new source to the data
        data[ip].add(source)
    return data

def show_calls():
    request = requests.get(url=server + "/api/commander/calls")
    if request.status_code != 200:
        print("{}:\n{}".format(request.status_code, request.content))
        return ""
    return request.text

def show_tasks():
    request = requests.get(url=server + "/api/commander/tasks")
    if request.status_code != 200:
        print("{}:\n{}".format(request.status_code, request.content))
        return ""
    return request.text

def show(args):
    if "recent" in args:
        data = show_recent()
        print("Recent Hosts:")
        for host in data:
            print("{}: {}".format(host, list(data[host])))
    elif "call" in args:
        print(show_calls())
    elif "task" in args:
        print(show_tasks())
    return


def help():
    print("Crowd Control client")
    print("export CC_SERVER or modify {} to change the server".format(sys.argv[0]))
    print()
    print("Current server: " + server)
    print("New task:                `t: host[ hosts...]: commands`")
    print("New task script:         `ts: host[ hosts...]: <script file>`")
    print("New task for IP file:    `th: <ip file>: commands`")
    print("Show recent hosts:       `s: recent`")
    print("Show callbacks log:      `s: calls`")
    print("Show tasks log:          `s: tasks`")
    quit("\nExample usage:\n\t{} t: 1.1.1.1 2.2.2.2 host3: echo hi".format(sys.argv[0]))

if __name__ == "__main__":
    # Get the server from the enivronment
    server = os.environ.get("CC_SERVER", "http://0.0.0.0:5000")
    # requests doesnt like it when there isnt a protocol
    if not server.startswith("http://") and not server.startswith("https://"):
        server = "http://" + server 
    # Remove trailing /
    server = server.rstrip('/')

    # Show the help if we need
    if len(sys.argv) < 2:
        help()
    else:
        args = " ".join(sys.argv[1:])
        if args.startswith("ts:") or args.startswith("t:"):
            new_task(args)
        elif args.startswith("s:"):
            show(args)
        else:
            help()