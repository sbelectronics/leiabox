from midistuff import all_notes_off

class Program(object):
    def __init__(self, ui):
        self.ui = ui
        for i in range(0, self.ui.num_buttons):
            self.ui.set_button_bright(i, 0)
        all_notes_off()

    def button_event(self, number, state):
        pass

    def idle(self):
        pass

    def background_play_complete(self, p):
        pass
