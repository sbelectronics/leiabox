"""
    leiabox_manager

    Used for integrating LeiaBox UI with django. Basically, launches the LeiaBox UI in a thread.
"""

import argparse
import smbus
import threading
from ui import LeiaUI

glo_leiabox = None

class LeiaUIThread(threading.Thread):
    def __init__(self, bus):
        super(LeiaUIThread, self).__init__()
        self.ui = LeiaUI(bus)
        self.daemon = True

    def run(self):
        self.ui.run_ui()

    def set_program(self, number):
        self.ui.set_program(number)

    def get_program(self):
        return self.ui.program_number

    def set_volume(self, *args, **kwarfs):
        self.ui.set_program(*args, **kwargs)

    def get_volume(self, volume):
        return self.ui.volume


def parse_args():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    return args

def startup(args):
    global glo_leiabox
   
    bus = smbus.SMBus(1)

    leiabox = LeiaUIsThread(bus)
    leiabox.start()

    glo_leiabox = leiabox
