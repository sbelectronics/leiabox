import mido
from midipercuss import HIGHTOM1, MUTHIGHCONGA, LOWCONGA, HIGHTIMBALE, SNAREDRUM1, LOWTOM2, MIDTOM1, CLAVES
from program import Program
from midistuff import connect_midi

class MusicProgram(Program):
    instruments = (14,  # xylophone
                   56,  # orch hit
                   74,  # flute
                   110) # bagpipes


    def __init__(self, ui):
        super(MusicProgram, self).__init__(ui)

        self.midi = connect_midi() # mido.open_output('FLUID Synth (966):Synth input port (966:0) 128:0')

        for i in range(0,4):
            # NOTE(smbaker): There's an off-by-one thing going on with instruments compared to my SC-55
            self.midi.send(mido.Message('program_change', program=self.instruments[i]-1, channel=i+1))

        #self.midi.send(mido.Message('program_change', program=114, channel=9))


    def get_note(self, r, c):
        notes = (60, 62, 64 , 65, 67, 69)
        percuss1_notes = (0, HIGHTOM1, MUTHIGHCONGA, LOWCONGA, HIGHTIMBALE)
        percuss2_notes = (0, SNAREDRUM1, LOWTOM2, MIDTOM1, CLAVES)
        if (r == 0):
            channel = 9
            note=percuss1_notes[c]
        elif (r == 5):
            channel = 9
            note=percuss2_notes[c]
        else:
            channel = r
            note=notes[c]
        return (note, channel)

    def button_event(self, number, state):
        row = self.ui.button_rows[number]
        column = self.ui.button_columns[number]

        (note, channel) = self.get_note(row, column)

        if state:
            self.ui.set_button_bright(number, 100)
            self.midi.send(mido.Message('note_on', note=note, channel=channel, velocity=127))
        else:
            self.ui.set_button_bright(number, 0)
            self.midi.send(mido.Message('note_off', note=note, channel=channel, velocity=127))

        
