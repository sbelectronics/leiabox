"""
    leiabox_manager

    Used for integrating LeiaBox UI with django. Basically, launches the LeiaBox UI in a thread.
"""

import argparse
import smbus
import threading
import time
from ui import LeiaUI

glo_leiabox = None

class LeiaUIThread(threading.Thread):
    def __init__(self, bus):
        super(LeiaUIThread, self).__init__()
        self.ui = LeiaUI(bus)
        self.daemon = True
        self.lock = threading.Lock()

    def run_lock_acquire(self):
        self.lock.acquire()

    def run_lock_release(self):
        self.lock.release()

    def run(self):
        try:
            while True:
                self.run_lock_acquire()
                try:
                    self.ui.run_ui_once()
                finally:
                    self.run_lock_release()
                time.sleep(0.01)
        finally:
            self.ui.all_notes_off()

    def set_program(self, number):
        self.ui.set_program(number)

    def get_program(self):
        return self.ui.program_number

    def set_volume(self, *args, **kwargs):
        self.ui.set_volume(*args, **kwargs)

    def get_volume(self):
        return self.ui.volume

    def button_down(self, number):
        self.run_lock_acquire()
        try:
            self.ui.button_event(number, True)
        finally:
            self.run_lock_release()

    def button_up(self, number):
        self.run_lock_acquire()
        try:
            self.ui.button_event(number, False)
        finally:
            self.run_lock_release()


def parse_args():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    return args

def startup(args):
    global glo_leiabox
   
    bus = smbus.SMBus(1)

    leiabox = LeiaUIThread(bus)
    leiabox.start()

    glo_leiabox = leiabox
