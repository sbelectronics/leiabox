import os
import mido

def connect_midi():
    for name in mido.get_output_names():
        if "FLUID" in name:
            return mido.open_output(name)
    raise Exception("Unable to find suitable midi device")

def all_notes_off():
    midi = connect_midi() # mido.open_output('FLUID Synth (966):Synth input port (966:0) 128:0')

    for i in range(0, 16):
        midi.send(mido.Message('control_change', control=123, value=0, channel=i))

def set_volume(amount):
    os.system("amixer sset PCM %d%%" % amount)