#! /bin/bash
set -e

cd /home/pi/leiabox

bash ./start_fluidsynth.sh

set +e
python ./midistuff.py
while [[ $? != 0 ]]; do
    echo "Waiting for midi to become available"
    python ./midistuff.py
done
set -e

nohup python ./web_server.py > /tmp/pi-leiabox.out 2> /tmp/pi-leiabox.err & 
