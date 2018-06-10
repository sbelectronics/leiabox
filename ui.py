"""
    LeiaBox User Interface
    Scott Baker, http://www.smbaker.com/
"""

import smbus
import time
from smbpi.tlc59116 import TLC59116, STATE_ON, STATE_OFF, STATE_PWM
from smbpi.ioexpand import MCP23017

from musicprogram import MusicProgram
from gameprogram import GameProgram
from midistuff import all_notes_off, set_volume

DEBOUNCE_TIME=0.01
LONG_THRESH=2

class LeiaUI(object):
    button_music = 4
    button_game = 10
    button_spell = 16
    button_shift = 21
    button_animals = 22
    button_off = 27

    button_v0 = 0
    button_v1 = 5
    button_v2 = 11
    button_v3 = 17
    button_v4 = 23
    button_v5 = 28

    volumes = (50,60,70,80,90,100)

    button_rows = (   1, 2, 3, 4,
                   0, 1, 2, 3, 4, 5,
                   0, 1, 2, 3, 4, 5,
                   0, 1, 2, 3, 4, 5,
                   0, 1, 2, 3, 4, 5,
                      1, 2, 3, 4)

    button_columns = (   0, 0, 0, 0,
                      1, 1, 1, 1, 1, 1,
                      2, 2, 2, 2, 2, 2,
                      3, 3, 3, 3, 3, 3,
                      4, 4, 4, 4, 4, 4,
                         5, 5, 5, 5)

    def __init__(self, bus):
        self.led_controllers = [TLC59116(bus, 0x60), TLC59116(bus, 0x61)]
        self.button_controllers = [MCP23017(bus, 0x20), MCP23017(bus, 0x21)]
        self.num_buttons = 32

        self.cached_inputs=[ [0,0], [0,0] ]

        self.brights=[]
        self.button_last_state = []
        self.button_last_time = []
        self.button_down_time = []
        self.button_long_event_sent = []
        for i in range(0, self.num_buttons):
            self.brights.append(-1)
            self.set_button_bright(i, 0)
            self.button_last_state.append(False)
            self.button_last_time.append(0)
            self.button_down_time.append(0)
            self.button_long_event_sent.append(False)

        for led_controller in self.led_controllers:
            led_controller.set_oscillator(True)

        for button_controller in self.button_controllers:
            for i in range(0, 2):
                button_controller.set_pullup(i, 0xFF)

        self.program = None
        self.set_program(0)

    def set_program(self, number):
        if (number == 0):
            self.program = MusicProgram(self)
        elif (number == 1):
            self.program = GameProgram(self)

    def set_button_bright(self, number, brightness):
        if brightness == self.brights[number]:
            # Nothing to do
            return

        #print "set", number, brightness

        chip = number / 16
        i = number % 16
        if brightness == 100:
            self.led_controllers[chip].set_led_state(i, STATE_ON)
        elif brightness > 0:
            self.led_controllers[chip].set_led_state(i, STATE_PWM)
            self.led_controllers[chip].set_led_pwm(i, brightness)
        else:
            self.led_controllers[chip].set_led_state(i, STATE_OFF)

        self.brights[number] = brightness

    def get_button_state(self, number):
        chip_number = number / 16
        chip = self.button_controllers[chip_number]
        chip_offset = number % 16
        bank = chip_offset / 8
        i = chip_offset % 8

        v = chip.get_gpio(bank)

        #print number, chip_number, chip, chip_offset, bank, i, v

        bit = (1 << i)
        return (v & bit) == 0

    def cache_inputs(self):
        for chip_number in range(0,2):
            for bank in range(0,2):
                chip = self.button_controllers[chip_number]
                self.cached_inputs[chip_number][bank] = chip.get_gpio(bank)

    def get_cached_button_state(self, number):
        chip_number = number / 16
        chip_offset = number % 16
        bank = chip_offset / 8
        i = chip_offset % 8

        v = self.cached_inputs[chip_number][bank]

        bit = (1 << i)
        return (v & bit) == 0

    def button_event(self, number, state):
        if self.program:
            self.program.button_event(number, state)

    def button_long_event(self, number):
        if self.button_last_state[self.button_shift]:
            if (number==self.button_music):
                self.set_program(0)
            elif (number==self.button_game):
                self.set_program(1)
            elif (number==self.button_v0):
                set_volume(self.volumes[0])
            elif (number==self.button_v1):
                set_volume(self.volumes[1])
            elif (number==self.button_v2):
                set_volume(self.volumes[2])
            elif (number==self.button_v3):
                set_volume(self.volumes[3])
            elif (number==self.button_v4):
                set_volume(self.volumes[4])
            elif (number==self.button_v5):
                set_volume(self.volumes[5])

    def process_buttons(self):
        self.cache_inputs()
        for i in range(0, self.num_buttons):
            state = self.get_cached_button_state(i)
            if state != self.button_last_state[i]:
                tNow=time.time()
                if (tNow-self.button_last_time[i] >= DEBOUNCE_TIME):
                    self.button_event(i, state)
                    self.button_last_time[i] = tNow
                    self.button_last_state[i] = state

            if state:
                if (not self.button_down_time[i]):
                    self.button_down_time[i] = time.time()
                elif (not self.button_long_event_sent[i]) and (time.time()-self.button_down_time[i] > LONG_THRESH):
                    self.button_long_event(i)
                    self.button_long_event_sent[i] = True
            else:
                self.button_down_time[i] = None
                self.button_long_event_sent[i] = False

    def run_ui(self):
        try:
            while True:
                self.process_buttons()
                if self.program:
                    self.program.idle()
                time.sleep(0.01)
        finally:
            all_notes_off()

    def run_test(self):
        lit = 0
        last_time = time.time()
        while True:
            for i in range(0, self.num_buttons):
                if (i==lit) or (self.get_button_state(i)):
                    self.set_button_bright(i, 100)
                else:
                    self.set_button_bright(i, 0)

            if (time.time() - last_time) > 0.1:
                lit = (lit + 1) % self.num_buttons
                last_time = time.time()

            time.sleep(0)  #0.001)


def main():
    bus = smbus.SMBus(1)
    ui = LeiaUI(bus)
    #ui.run_test()
    ui.run_ui()

if __name__ == "__main__":
    main()
