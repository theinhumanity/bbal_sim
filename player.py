import random
from config import *


class Player:
    def __init__(self, name: str,
                 shot_accuracy: float = None, rebounding: float = None, defense: float = None):
        if not name: raise ValueError("Name cannot be empty")

        if shot_accuracy:
            if shot_accuracy < 0: raise ValueError("Shot accuracy must be >= 0")
            if shot_accuracy > 1: raise ValueError("Shot accuracy must be <= 1")

        if rebounding:
            if rebounding < 0: raise ValueError("Rebounding must be >= 0")
            if rebounding > 1: raise ValueError("Rebounding must be <= 1")

        if defense:
            if defense < 0: raise ValueError("Defense must be >= 0")
            if defense > 1: raise ValueError("Defense must be <= 1")

        self.name = name

        if shot_accuracy:
            self.shot_accuracy = shot_accuracy
        else:
            self.shot_accuracy: float = clamp(random.normalvariate(SHOOTING_EFFICIENCY_MEAN, SHOOTING_EFFICIENCY_SD))

        if rebounding:
            self.rebounding = rebounding
        else:
            self.rebounding: float = clamp(random.normalvariate(REBOUNDING_MEAN, REBOUNDING_SD))

        if defense:
            self.defense = defense
        else:
            self.defense: float = clamp(random.normalvariate(DEFENSE_MEAN, DEFENSE_SD))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Player(name={self.name!r}, shot_accuracy={self.shot_accuracy:.2f}, rebounding={self.rebounding:.2f}, defense={self.defense:.2f})"


def clamp(value: float, minimum: float=0, maximum: float=1) -> float:
    if value < minimum:
        return minimum
    elif value > maximum:
        return maximum
    else:
        return value