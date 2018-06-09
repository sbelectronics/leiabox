import time
import random
import subprocess

class PlaySong(object):
    songs = ["mpg123 -k 1755 -n 700 mp3/Queen-AnotherOneBitesTheDust.mp3"]

    def __init__(self, ui):
        self.ui = ui

    def play_song(self, index):
        song_cmd = self.songs[index]

        p = subprocess.Popen(song_cmd, shell=True)
        while p.poll() is None:
            for i in range(0,self.ui.num_buttons):
                self.ui.set_button_bright(i, random.randint(0,1) * 100)
            time.sleep(0.05)

        for i in range(0, self.ui.num_buttons):
            self.ui.set_button_bright(i, 0)






