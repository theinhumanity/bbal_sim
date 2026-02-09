import random

from player import Player


class Game:
    def __init__(self, team1: list[Player], team2: list[Player],
                 regulation_periods: int=4, regulation_period_length: int= 12 * 60,
                 overtime_length: int = 5 * 60,
                 shot_clock_length: int=24,
                 players_on_court: int= 3):
        if regulation_periods < 1: raise ValueError("Periods must be >= 1")
        if regulation_period_length < 1: raise ValueError("Period length must be >= 1")
        if shot_clock_length < 1: raise ValueError("Shot clock must be >= 1")
        if shot_clock_length > regulation_period_length: raise ValueError("Shot clock must be <= period seconds")
        if len(team1) != players_on_court: raise ValueError("Team 1 length is wrong")
        if len(team2) != players_on_court: raise ValueError("Team 2 length is wrong")

        self.team1 = team1
        self.team2 = team2
        self.regulation_periods = regulation_periods
        self.regulation_period_length = regulation_period_length

        self.overtime_length = overtime_length

        self.shot_clock_length = shot_clock_length

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

        for period in range(self.regulation_periods):
            print(f"Q{period + 1}")

            self.sim_period(self.regulation_period_length)

        overtimes: int = 0

        while self.team1_score == self.team2_score:
            print(f"{overtimes + 1 if overtimes > 0 else ""}OT")
            overtimes += 1

            self.sim_period(self.overtime_length)

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
        if period_time > self.shot_clock_length:
            time_elapsed = random.randrange(1, self.shot_clock_length)
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
