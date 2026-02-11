import tkinter as tk

from game import Game
from config import *


class DisplayGame:
    def __init__(self):
        self.root = tk.Tk()

        self.period_label = tk.Label(self.root, text="Q1")
        self.period_label.grid(row=0, column=0)

        self.score_label = tk.Label(self.root, text="0 - 0")
        self.score_label.grid(row=0, column=1)

        self.time_label = tk.Label(self.root, text="12:00")
        self.time_label.grid(row=0, column=2)

        self.play_label = tk.Label(self.root, text="", width=50)
        self.play_label.grid(row=1, columnspan=3)

        self.next_play_button = tk.Button(self.root, text="Next Play")
        self.next_play_button.grid(row=2, columnspan=3)

    def display_game(self, game: Game):
        events = game.event_list
        index = -1

        def update_label():
            nonlocal index

            index += 1

            if index >= len(events):
                self.period_label.config(text="00:00")
                return

            event_msg, event_type = events[index]

            while index + 1 < len(events) and event_type not in TYPES_TO_DISPLAY:
                if event_type is Event.PERIOD:
                    self.period_label.config(text=event_msg)
                elif event_type is Event.SCORE_DISPLAY:
                    self.score_label.config(text=event_msg)
                elif event_type is Event.TIME_DISPLAY:
                    self.time_label.config(text=event_msg)
                elif event_type is Event.WINNER:
                    self.next_play_button.config(state=tk.DISABLED)
                    self.time_label.config(text='00:00')

                index += 1
                event_msg, event_type = events[index]

            self.play_label.config(text=event_msg)

        self.next_play_button.configure(command=update_label)

        self.root.mainloop()


