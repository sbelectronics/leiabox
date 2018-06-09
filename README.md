This is a toy I'm building for Leia.

Make sure to install smb-pi-lib, from https://github.com/sbelectronics/smb-pi-lib


Audio Setup

See 
https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/raspberry-pi-usage
https://www.raspberrypi.org/forums/viewtopic.php?t=33431

/boot/config.txt
```
# dtparam=audio=on
dtoverlay=hifiberry-dac
dtoverlay=i2s-mmap
```

/etc/asound.conf
```
#pcm.!default  {
#   type hw card 0
#}
#ctl.!default {
#   type hw card 0
#}
pcm.speakerbonnet {
       type hw card 0
}
     
pcm.dmixer {
       type dmix
       ipc_key 1024
       ipc_perm 0666
       slave {
         pcm "speakerbonnet"
         period_time 0
         period_size 1024
         buffer_size 8192
         rate 44100
         channels 2
       }
}
     
ctl.dmixer {
        type hw card 0
}

pcm.monocard {
  slave.pcm dmixer
  slave.channels 2
  type route
  ttable {
    # Nothing to output channel 0 (Left).
    0.0 0
    1.0 0
    # Copy both input channels  to output channel 1 (Right).
    0.1 0.5
    1.1 0.5
  }
}

ctl.monocard {
  type hw
  card 1
}

pcm.softvol {
        type softvol
#        slave.pcm "dmixer"
        slave.pcm monocard
        control.name "PCM"
        control.card 0
}
     
ctl.softvol {
        type hw card 0
}
     
pcm.!default {
        type             plug
        slave.pcm       "softvol"
}
```

test
```
speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav 
```