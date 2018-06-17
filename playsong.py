import os
import time
import random
import subprocess
import threading

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


class BackgroundPlayer(threading.Thread):
    def __init__(self, ui):
        super(BackgroundPlayer, self).__init__()
        self.ui=ui
        self.plays=[]
        self.daemon = True

    def add_file(self, dir=None, fn=None, tag=None, data={}):
        data = data.copy()

        if dir:
            fn = os.path.join(dir, fn)
        if fn:
            data["fn"] = fn
        if tag:
            data["tag"] = tag

        song_cmd = "mpg123 %s" % fn
        data["p"] = subprocess.Popen(song_cmd, shell=True)
        self.plays.append(data)

    def cancel(self, tag=None):
        for p in self.plays[:]:
            if (not tag) or (p.get(tag)==tag):
                p["p"].terminate()

    def run(self):
        while True:
            for p in self.plays[:]:
                if p["p"].poll() is not None:
                    self.ui.background_play_complete(p)
                    self.plays.remove(p)
            time.sleep(0.01)
