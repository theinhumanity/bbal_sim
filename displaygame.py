import tkinter as tk

import utils
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
        self.next_play_button.grid(row=2, column=1)

        self.next_period_button = tk.Button(self.root, text="Next Period")
        self.next_period_button.grid(row=2, column=2)

    def display_game(self, game: Game):
        events = game.event_list
        index = 0

        def update_label(events_to_stop: list[Event]):
            nonlocal index

            index += 1

            if index >= len(events):
                self.period_label.config(text=utils.format_time(0))
                return

            event_msg, event_type = events[index]

            while index + 1 < len(events) and event_type not in events_to_stop:
                if event_type in PERIOD_EVENTS:
                    self.period_label.config(text=event_msg)
                elif event_type in PLAY_EVENTS:
                    self.play_label.config(text=event_msg)
                elif event_type is Event.SCORE_DISPLAY:
                    self.score_label.config(text=event_msg)
                elif event_type is Event.TIME_DISPLAY:
                    self.time_label.config(text=event_msg)
                elif event_type is Event.WINNER:
                    self.next_play_button.config(state=tk.DISABLED)
                    self.next_period_button.config(state=tk.DISABLED)
                    self.time_label.config(text=utils.format_time(0))

                index += 1
                event_msg, event_type = events[index]
            if event_type in PERIOD_EVENTS:
                self.period_label.config(text=event_msg)
                if event_type is Event.REGULATION_PERIOD:
                    self.time_label.config(text=utils.format_time(REGULATION_PERIOD_LENGTH))
                elif event_type is Event.OVERTIME_PERIOD:
                    self.time_label.config(text=utils.format_time(OVERTIME_PERIOD_LENGTH))
            elif event_type in PLAY_EVENTS:
                self.play_label.config(text=event_msg)

        def next_play():
            update_label(PLAY_EVENTS)

        def next_period():
            update_label(PERIOD_EVENTS)

        self.next_play_button.configure(command=next_play)
        self.next_period_button.configure(command=next_period)

        self.root.mainloop()


