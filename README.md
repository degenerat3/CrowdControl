# CrowdControl
This project is a C2 that utilizes web requests to deliver commands.  This repo contains the server/client/controller.  The server is a docker container which runs a flask app, the controller is a python script which allows users to push commands to the server, and the client(s) are a series of golang programs and bash scripts that will invoke the proper web request to pull commands, then execute them.  

## Server
The server is a docker container that's running alpine linux with flask.  All the server functions/endpoints can be found in the `app.py` file.  

#### Endpoints
The server has the following endpoints:
 - `'/<ip>/<typ>' or '/api/callback/<ip>/<typ>'` - these are the endpoints the clients will hit in order to receive their commands.  The former is preferred, as the latter will soon be phased out.  The "\<ip>" is the ip of the client that's calling back, and the "\<type>" denotes where the callback is coming from (bash script, golang binary, vimrc) which is used for logging purposes.
  - `'/api/commander/push'` - this is the endpoint that the commander script/CLI will send commands to.  It accepts a JSON POST that contains the target hosts and commands to be executed.
  - `'/api/commander/calls'` - this is an endpoint that serves a log.  It's returns the log that tracks all client callbacks.  Any time a client hits one of the callback endpoints, an entry is made containing "Time | IP | Type", this endpoint returns all entires
  - `'/api/commander/tasks'` - this is the other endpoint that serves a log.  Any time a command is pushed to the server, an entry is added to the task log containing "Time | Targets | Tasks", this endpoint returns all entires.  

## Controller
There are two methods to send commands to the server.  The original method, `commander.py` is a CLI with the ability to view tracked hosts, set multiple targets, and set commands.  This method is being phased out in favor of `mace.py`.  The `mace` script is not a CLI, but rather all input is given through arguments, to allow for faster/easier control.  The following are options when executing the mace script:  
```
FUNCTION:                ARGUMENTS TO PASS TO MACE.PY:
New task:                t: host[ hosts...]: commands 
New task script:         ts: host[ hosts...]: \<script file>  
Show recent hosts:       s: recent
Show callbacks log:      s: calls
Show tasks log:          s: tasks
Example:                 t: 1.1.1.1 2.2.2.2 host3: echo hi" 
```  
'New task' will run the given commands on the specified hosts.  'New task script' will execute the given script on the specified hosts.  'Show recent hosts' will list all hosts that have called back in the last 10 minutes, and the 'show log' options will display the specified log to the user.  

'New task' and 'New task script' both support "groups." You can define a group by creating a file with the following format:  
```
8.8.8.8
1.2.3.4
10.100.6.9
```
The file must be in exactly the format shown above, with each IP on it's own line and no other data in the file.  Once you have the group created, for example lets say we have the `web` group file, we can execute commands like this:  
`t: web: echo hi`  
or like this:  
`ts: web: script.sh`  
This will execute the given command or script on every IP listed in the group file.  Group files don't need to be in any specific place, but it's recommended to put them in their own "groups" directory inside the commander directory for easy reading.

## Clients
There is currently only support for Linux clients, although Windows endpoints have been created, so it's a WIP.  The client script can be anything from a golang binary, a python or bash script, etc, as long as it can invoke a web request.  The format is very simple, simply send a GET request to `serverIP/<ip>/<type>` and the return will be the commands that need to be executed.  

 ## Install and Configuration
 #### Server
The docker image can be built from the "server" directory by using the following command:  
`sudo docker build -t cc:latest .`  
once the build is finished, it can be run with the following:  
`sudo docker run -d -p 5000:5000 cc`  
The flask server is now accessible via port 5000  
#### Commander
In the `commander.py` file, the server variable needs to be set to the ip of the flask server.

## Future Work:
 - Windows endpoints have been created, we need to write some clients that will use cmd and/or PowerShell (preferably PowerShell).
 
 - Write a stager script that will pull a client script/binary/whatever, set it up as a scheduled task/service/whatever.  Once this stager script is hosted on the server (must make a new stager endpoint), hosts can be added to the control infrastucture by simply invoking a web request and piping the script into bash/PowerShell.
