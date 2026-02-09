import random
from config import *


class Player:
    def __init__(self, name: str):
        self.name = name
        self.shot_accuracy: float = random.normalvariate(SHOOTING_EFFICIENCY_MEAN, SHOOTING_EFFICIENCY_SD)
        self.clamp_shot_accuracy()

    def clamp_shot_accuracy(self):
        if self.shot_accuracy < 0:
            self.shot_accuracy = 0
        if self.shot_accuracy > 1:
            self.shot_accuracy = 1

    def __str__(self):
        return f"{self.name} ({self.shot_accuracy})"

    def __repr__(self):
        return f"Player(name={self.name!r}, shot_accuracy={self.shot_accuracy:.2f})"
