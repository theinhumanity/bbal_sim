import random
from typing import Tuple

PLAYERS_ON_COURT: int = 2

class Player:
    def __init__(self, name: str):
        self.name = name
        self.shot_accuracy: float = random.normalvariate(0.5, 0.15)
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

class Game:
    def __init__(self, team1: list[Player], team2: list[Player],
                 periods: int=4, period_seconds: int= 12 * 60, shot_clock_seconds: int=24):
        if periods < 1: raise ValueError("Periods must be >= 1")
        if period_seconds < 1: raise ValueError("Period length must be >= 1")
        if shot_clock_seconds < 1: raise ValueError("Shot clock must be >= 1")
        if shot_clock_seconds > period_seconds: raise ValueError("Shot clock must be <= period seconds")
        if len(team1) != PLAYERS_ON_COURT: raise ValueError("Team 1 length is wrong")
        if len(team2) != PLAYERS_ON_COURT: raise ValueError("Team 2 length is wrong")

        self.team1 = team1
        self.team2 = team2
        self.periods = periods
        self.period_seconds = period_seconds
        self.shot_clock_seconds = shot_clock_seconds

        self.team1_score: int = 0
        self.team2_score: int = 0

        self.offense: list[Player] = team1

        self.boxscore: dict[Player, int] = {}

        for player in self.team1 + self.team2:
            self.boxscore[player] = 0

    def sim_game(self) -> None:
        print(self.team1, self.team2)

        for period in range(self.periods):
            print(f"Q{period + 1}")

            self.sim_period()

        if self.team1_score > self.team2_score:
            print(f"Team 1 {self.team1} won by {self.team1_score - self.team2_score} points!!!")
        elif self.team2_score > self.team1_score:
            print(f"Team 2 {self.team2} won by {self.team2_score - self.team1_score} points!!!)")
        else:
            print("Tie.")

        for player in self.team1 + self.team2:
            print(f"{player.name} scored {self.boxscore[player]} points")


    def sim_period(self) -> None:
        period_time: int = self.period_seconds
        while period_time > 0:
            time_elapsed = self.sim_possession(period_time)
            period_time -= time_elapsed

            self.offense = self.team2 if self.offense is self.team1 else self.team1

            print(print_time(period_time))
            print(print_score(self.team1_score, self.team2_score))

    def sim_possession(self, period_time: int) -> int:
        if period_time > self.shot_clock_seconds:
            time_elapsed = random.randrange(1, self.shot_clock_seconds)
        else:
            time_elapsed = period_time
        period_time -= time_elapsed
        if self.offense is self.team1:
            player, points = shot_attempt(self.team1)
            self.team1_score += points
        else:
            player, points = shot_attempt(self.team2)
            self.team2_score += points

        print(print_shot_attempts(player, points))

        self.boxscore[player] += points

        return time_elapsed


def shot_attempt(team: list[Player]) -> tuple[Player, int]:
    player: Player = random.choice(team)

    points: int = 0

    if random.random() < player.shot_accuracy:
        points += 2

    return player, points


def print_time(period_time) -> str:
    return f"{period_time // 60 :02}:{period_time % 60 :02}"


def print_score(team1_score, team2_score) -> str:
    return f"{team1_score} - {team2_score}"


def print_shot_attempts(player, points) -> str:
    if points > 0:
        return f"{player.name} scored {points} points!"
    else:
        return f"{player.name} missed!"

def main() -> None:
    team1: list[Player] = [Player('Jille'), Player('Adam')]
    team2: list[Player] = [Player('Mauk'), Player('Kazuki')]

    game: Game = Game(team1, team2)

    game.sim_game()


if __name__ == '__main__':
    main()