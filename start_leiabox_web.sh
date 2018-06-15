#! /bin/bash
cd /home/pi/pi-leiabox

nohup python ./web_server.py > /tmp/pi-leiabox.out 2> /tmp/pi-leiabox.err & 
