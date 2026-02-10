import random
from config import *


class Player:
    def __init__(self, name: str):
        self.name = name

        self.shot_accuracy: float = clamp(random.normalvariate(SHOOTING_EFFICIENCY_MEAN, SHOOTING_EFFICIENCY_SD))
        self.rebounding: float = clamp(random.normalvariate(REBOUNDING_MEAN, REBOUNDING_SD))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Player(name={self.name!r}, shot_accuracy={self.shot_accuracy:.2f}, rebounding={self.rebounding:.2f})"


def clamp(value: float, minimum: float=0, maximum: float=1) -> float:
    if value < minimum:
        return minimum
    elif value > maximum:
        return maximum
    else:
        return value