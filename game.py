import random

from player import Player
from config import *


class Game:
    def __init__(self, team1: list[Player], team2: list[Player]):
        if len(team1) != PLAYERS_ON_COURT: raise ValueError("Team 1 length is wrong")
        if len(team2) != PLAYERS_ON_COURT: raise ValueError("Team 2 length is wrong")

        self.team1 = team1
        self.team2 = team2

        self.team1_score: int = 0
        self.team2_score: int = 0

        self.offense: list[Player] = team1

        self.boxscore: dict[Player, int] = {}
        for player in self.team1 + self.team2:
            self.boxscore[player] = 0

        self.game_seconds_played = 0

        # (game_seconds_played, team1_score, team2_score)
        self.score_history: list[tuple[int, int, int]] = []

    def sim_game(self) -> None:
        print(self.team1, self.team2)

        for period in range(REGULATION_PERIODS):
            print(f"Q{period + 1}")

            self.sim_period(REGULATION_PERIOD_LENGTH)

        overtimes: int = 0

        while self.team1_score == self.team2_score:
            print(f"{overtimes + 1 if overtimes > 0 else ""}OT")
            overtimes += 1

            self.sim_period(OVERTIME_PERIOD_LENGTH)

        self.handle_winner()

    def sim_period(self, period_length: int) -> None:
        period_time: int = period_length
        while period_time > 0:
            time_elapsed = self.sim_possession(period_time)
            period_time -= time_elapsed

            self.offense = self.team2 if self.offense is self.team1 else self.team1

            print(print_time(period_time))
            print(print_score(self.team1_score, self.team2_score))

            self.game_seconds_played += time_elapsed
            self.score_history.append((self.game_seconds_played, self.team1_score, self.team2_score))

    def sim_possession(self, period_time: int) -> int:
        if period_time > SHOT_CLOCK_LENGTH:
            time_elapsed = random.randrange(1, SHOT_CLOCK_LENGTH)
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

    def handle_winner(self):
        if self.team1_score > self.team2_score:
            print(f"Team 1 {self.team1} won by {self.team1_score - self.team2_score} points!!!")
        elif self.team2_score > self.team1_score:
            print(f"Team 2 {self.team2} won by {self.team2_score - self.team1_score} points!!!)")
        else:
            print("Tie.")
        for player in self.team1 + self.team2:
            print(f"{player.name} scored {self.boxscore[player]} points")


def shot_attempt(team: list[Player]) -> tuple[Player, int]:
    player: Player = random.choices(
        team,
        weights=[p.shot_accuracy for p in team],
        k=1
    )[0]

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
