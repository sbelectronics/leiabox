#! /bin/bash
pgrep fluidsynth
if [[ $? == 0 ]]; then
   echo "Fluidsynth is already running"
else 
   nohup fluidsynth -a alsa -i /usr/share/sounds/sf2/FluidR3_GM.sf2 -r=22050 -s > /tmp/fluidsynth.out 2> /tmp/fluidsynth.err & 
fi

