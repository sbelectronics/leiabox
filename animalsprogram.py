import os
import time

from program import Program

class AnimalsProgram(Program):
    def __init__(self, ui):
        super(AnimalsProgram, self).__init__(ui)

        self.button_play_count=[]
        for i in range(0, ui.num_buttons):
            self.button_play_count.append(0)

    def button_event(self, number, state):
        button_letter = {0: "A",
                         1: "G",
                         2: "M",
                         3: "S",
                         5: "B",
                         6: "H",
                         7: "N",
                         8: "T",
                         9: "Y",
                        11: "C",
                        12: "I",
                        13: "O",
                        14: "U",
                        15: "Z",
                        17: "D",
                        18: "J",
                        19: "P",
                        20: "V",
                        23: "E",
                        24: "K",
                        25: "Q",
                        26: "W",
                        28: "F",
                        29: "L",
                        30: "R",
                        31: "X"}

        animals = { "A": "anteater",
                    "B": "bear",
                    "C": "cat",
                    "D": "dog",
                    "E": "elephant",
                    "F": "frog",
                    "G": "geese",
                    "H": "horse",
                    "I": "impala_boosted",
                    "J": "jaguar",
                    "K": "koala",
                    "L": "lion",
                    "M": "monkey",
                    "N": "nighthawk_cropped_boosted",
                    "O": "owl",
                    "P": "pig",
                    "Q": "quail_cropped_boosted",
                    "R": "raccoon_cropped",
                    "S": "sheep",
                    "T": "turkey",
                    "U": "umbrellabird",
                    "V": "vulture",
                    "W": "wolf",
                    "X": "xenops_cropped_boosted",
                    "Y": "yellowjacket_cropped_boosted",
                    "Z": "zebra" }

        if (state):
            if number not in button_letter:
                return
            letter = button_letter[number]

            self.ui.set_button_bright(number, 100)
            self.button_play_count[number] += 1
            self.ui.background_play(fn=animals[letter]+".mp3", dir="animals", tag="animals", data={"button": number})

    def background_play_complete(self, p):
        button = p.get("button", None)
        if button is not None:
            self.button_play_count[button] -= 1
            if (self.button_play_count[button] <= 0):
                self.ui.set_button_bright(button, 0)
