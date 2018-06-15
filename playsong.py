import time
import random
import subprocess

class PlaySong(object):
    songs = ["mpg123 -k 1755 -n 700 mp3/Queen-AnotherOneBitesTheDust.mp3",
             "mpg123 -k 870 -n 800 --scale 24000 mp3/blondie-onewayoranother.mp3",
             "mpg123 -k 1170 -n 550 --scale 20000 mp3/patbenatar-hitmewithyourbestshot.mp3",
             "mpg123 -k 6150 -n 650 mp3/gapband-youdroppedabombonme.mp3",
             "mpg123 -k 2870 -n 700 --scale 14000 mp3/quietriot-bangyourhead.mp3",
             "mpg123 -k 850 -n 560 --scale 10000 mp3/joanjett-cherrybomb.mp3",
             "mpg123 -k 900 -n 520 --scale 16384 mp3/toddlundgren-bangthedrumallday.mp3",
             "mpg123 -k 3800 -n 620 --scale 20000 mp3/gogos-wegotthebeat.mp3"]

    def __init__(self, ui):
        self.ui = ui

    def play_song(self, index):
        index = index % len(self.songs)

        song_cmd = self.songs[index]

        p = subprocess.Popen(song_cmd, shell=True)
        while p.poll() is None:
            for i in range(0,self.ui.num_buttons):
                self.ui.set_button_bright(i, random.randint(0,1) * 100)
            time.sleep(0.05)

        for i in range(0, self.ui.num_buttons):
            self.ui.set_button_bright(i, 0)






