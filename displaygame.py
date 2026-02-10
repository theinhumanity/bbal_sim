import tkinter as tk

from game import Game
from config import *


class DisplayGame:
    def __init__(self):
        self.root = tk.Tk()

        self.play_label = tk.Label(self.root, text="", width=50)
        self.play_label.pack()

        self.next_play_button = tk.Button(self.root, text="Next Play")
        self.next_play_button.pack()

    def display_game(self, game: Game):
        events = game.event_list
        index = 0

        def update_label():
            nonlocal index

            index += 1

            if index >= len(events):
                return

            event_msg, event_type = events[index]

            while (event_type not in TYPES_TO_DISPLAY
                   and index + 1 < len(events)):
                index += 1
                event_msg, event_type = events[index]

            self.play_label.configure(text=event_msg)

        self.next_play_button.configure(command=update_label)

        self.root.mainloop()


