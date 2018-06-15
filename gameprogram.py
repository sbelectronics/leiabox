import mido
import random
import time

from musicprogram import MusicProgram
from playsong import PlaySong

JUMP_DELAY = 1

class GameProgram(MusicProgram):
    def __init__(self, ui):
        super(GameProgram, self).__init__(ui)

        self.button_jump_time = []
        for i in range(0, ui.num_buttons):
            self.button_jump_time.append(0)

        self.last_button = None
        self.last_jump_time = 0

    def idle(self):
        tNow = time.time()
        if (tNow - self.last_jump_time) > JUMP_DELAY:
            self.jump()

        if (self.last_button is not None) and ((tNow - self.last_jump_time) > self.hide_delay):
            self.hide()

    def hide(self):
        if (self.last_button is not None):
            self.ui.set_button_bright(self.last_button, 0)

            row = self.ui.button_rows[self.last_button]
            column = self.ui.button_columns[self.last_button]
            (note, channel) = self.get_note(row, column)
            self.midi.send(mido.Message('note_off', note=note, channel=channel, velocity=127))

            self.last_button = None

            self.hide_delay = self.hide_delay + 0.01

    def jump(self):
        self.hide()

        self.last_button = random.randint(0, self.ui.num_buttons-1)
        self.ui.set_button_bright(self.last_button, 100)

        row = self.ui.button_rows[self.last_button]
        column = self.ui.button_columns[self.last_button]
        (note, channel) = self.get_note(row, column)
        self.midi.send(mido.Message('note_on', note=note, channel=channel, velocity=127))

        self.last_jump_time = time.time()

        self.hide_delay = 0.5

        self.button_jump_time[self.last_button] = time.time()

    def button_event(self, number, state):
        if (state):
            elap = time.time() - self.button_jump_time[number]
            if (elap < self.hide_delay*2):
                self.hide()
                PlaySong(self.ui).play_song(number)
