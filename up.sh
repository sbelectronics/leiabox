rsync -avz --exclude "__history" --exclude "*~" --exclude "*.gif" --exclude "*.JPG" -e ssh . pi@leiabox.lan:/home/pi/leiabox/
