Install notes

```bash
# django
sudo pip install Django==1.7

# setup autostart
sudo crontab -e
  @reboot bash /home/pi/leiabox/start_leiabox_web.sh &> /dev/null

# be nice to the sd card
sudo emacs /etc/fstab
  tmpfs    /tmp            tmpfs    defaults,noatime,nosuid,size=100m    0 0
  tmpfs    /var/tmp        tmpfs    defaults,noatime,nosuid,size=30m    0 0
  tmpfs    /var/log        tmpfs    defaults,noatime,nosuid,mode=0755,size=100m    0 0
  tmpfs    /var/runxx        tmpfs    defaults,noatime,nosuid,mode=0755,size=2m    0 0
```
