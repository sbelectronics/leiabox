"""
    LeiaBox User Interface
    Scott Baker, http://www.smbaker.com/
"""

import smbus
import time
from smbpi.tlc59116 import TLC59116, STATE_ON, STATE_OFF, STATE_PWM
from smbpi.ioexpand import MCP23017

from musicprogram import MusicProgram

DEBOUNCE_TIME=0.01

class LeiaUI(object):
    button_rows = (1, 2, 3, 4,
                   0, 1, 2, 3, 4, 5,
                   0, 1, 2, 3, 4, 5,
                   0, 1, 2, 3, 4, 5,
                   1, 2, 3, 4)

    button_columns = (0, 0, 0, 0,
                      1, 1, 1, 1, 1, 1,
                      2, 2, 2, 2, 2, 2,
                      3, 3, 3, 3, 3, 3,
                      4, 4, 4, 4, 4, 4,
                      5, 5, 5, 5)

    def __init__(self, bus):
        self.led_controllers = [TLC59116(bus, 0x60), TLC59116(bus, 0x61)]
        self.button_controllers = [MCP23017(bus, 0x20), MCP23017(bus, 0x21)]
        self.num_buttons = 32

        self.brights=[]
        for i in range(0, self.num_buttons):
            self.brights.append(-1)
            self.set_button_bright(i, 0)
            self.button_last_state[i] = False
            self.button_last_time[i] = 0

        for led_controller in self.led_controllers:
            led_controller.set_oscillator(True)

        for button_controller in self.button_controllers:
            for i in range(0, 2):
                button_controller.set_pullup(i, 0xFF)

        self.program = None
        self.set_program(0)

    def set_program(self, number):
        if (number == 0):
            self.program = MusicProgram()

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

    def button_event(self, number, state):
        if self.program:
            self.program.button_event(number, state)

    def process_buttons(self):
        for i in range(0, self.num_buttons):
            state = self.get_button_state(i)
            if state != self.button_last_state[i]:
                tNow=time.time()
                if (tNow-self.button_last_time[i] >= DEBOUNCE_TIME):
                    self.button_event(i, state)
                    self.button_last_time[i] = tNow
                    self.button_last_state[i] = state

    def run_ui(self):
        while True:
            self.process_buttons()
            if self.program:
                self.program.idle()
            time.sleep(0.01)

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

            time.sleep(0.001)


def main():
    bus = smbus.SMBus(1)
    ui = LeiaUI(bus)
    #ui.run_test()
    ui.

if __name__ == "__main__":
    main()
