import mido

def all_notes_off():
    midi = mido.open_output('FLUID Synth (966):Synth input port (966:0) 128:0')

    for i in range(0, 16):
        midi.send(mido.Message('control_change', control=123, value=0, channel=i))
