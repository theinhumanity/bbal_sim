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

        self.most_recent_scorer: int = 0

        self.offense: list[Player] = team1
        self.defense: list[Player] = team2

        self.boxscore: dict[Player, dict[str, int]] = {}
        for player in self.team1 + self.team2:
            self.boxscore[player] = {
                'points': 0,
                'rebounds': 0,
            }

        self.game_seconds_played: int = 0

        # (game_seconds_played, team1_score, team2_score)
        self.score_history: list[tuple[int, int, int]] = []

        self.event_list: list[tuple[str, Event]] = []

    def log(self, msg: str, event_type: Event) -> None:
        #print(msg)
        self.event_list.append((msg, event_type))

    def sim_game(self) -> None:
        print(self.team1, self.team2)

        for period in range(REGULATION_PERIODS):
            self.log(f"Q{period + 1}", Event.PERIOD)

            self.sim_period(REGULATION_PERIOD_LENGTH)

        overtimes: int = 0

        while self.team1_score == self.team2_score:
            self.log(f"{overtimes + 1 }OT" if overtimes > 0 else "OT", Event.PERIOD)
            overtimes += 1

            self.sim_period(OVERTIME_PERIOD_LENGTH)

        self.handle_winner()

    def sim_period(self, period_length: int) -> None:
        period_time: int = period_length
        while period_time > 0:
            self.log(self.print_time(period_time), Event.TIME_DISPLAY)

            time_elapsed = self.sim_possession(period_time)
            period_time -= time_elapsed

            self.log(self.print_score(), Event.SCORE_DISPLAY)

            self.game_seconds_played += time_elapsed
            self.score_history.append((self.game_seconds_played, self.team1_score, self.team2_score))

    def sim_possession(self, period_time: int) -> int:
        possession_over: bool = False
        time_elapsed: int = 0

        while not possession_over and period_time > 0:
            if period_time - time_elapsed > SHOT_CLOCK_LENGTH:
                time_elapsed += random.randrange(1, SHOT_CLOCK_LENGTH)
            else:
                time_elapsed = period_time

            player, points = self.shot_attempt()

            if self.offense is self.team1:
                self.team1_score += points
            else:
                self.team2_score += points

            self.log(self.print_shot_attempt(player, points), Event.SCORE_DISPLAY)
            self.boxscore[player]['points'] += points

            if points > 0: # Scored, possession over
                possession_over = True
                self.most_recent_scorer = 1 if self.offense is self.team1 else 2
                self.switch_possession()
            else:
                rebounder: Player = self.rebound()
                self.log(self.print_rebound(rebounder), Event.REBOUND)
                self.boxscore[rebounder]['rebounds'] += 1

                if rebounder in self.offense: # Offensive rebound, possession continues
                    continue
                elif rebounder in self.defense: # Defensive rebound, possession over
                    possession_over = True
                    self.most_recent_scorer = 0
                    self.switch_possession()
                else:
                    raise ValueError("Rebounder neither of offense or defense!")

        return time_elapsed

    def switch_possession(self):
        self.offense, self.defense = self.defense, self.offense


    def handle_winner(self):
        if self.team1_score > self.team2_score:
            self.log(f"Team 1 {self.team1} won by {self.team1_score - self.team2_score} points!!!", Event.WINNER)
        elif self.team2_score > self.team1_score:
            self.log(f"Team 2 {self.team2} won by {self.team2_score - self.team1_score} points!!!", Event.WINNER)
        else:
            raise ValueError("Game ended in a tie!")

        for player in self.team1 + self.team2:
            self.log(f"{player.name} scored {self.boxscore[player]['points']} points and grabbed {self.boxscore[player]['rebounds']} rebounds", Event.BOXSCORE)


    def print_rebound(self, rebounder: Player) -> str:
        color = self.get_color(rebounder)

        if rebounder in self.offense:
            return f"{color}{rebounder.name} grabbed the offensive rebound!{END}"
        elif rebounder in self.defense:
            return f"{color}{rebounder.name} secured the defensive rebound.{END}"
        else:
            raise ValueError(f"Player not on offense or defense!")


    def print_shot_attempt(self, player: Player, points: int) -> str:
        color = self.get_color(player)

        if points > 0:
            return f"{color}{player.name} scored {points} points!{END}"
        else:
            return f"{color}{player.name} missed!{END}"

    def get_color(self, player: Player) -> str:
        if player in self.team1:
            return RED
        elif player in self.team2:
            return BLUE
        else:
            raise ValueError(f"Player not on team 1 or team 2!")


    def shot_attempt(self) -> tuple[Player, int]:
        player: Player = random.choices(
            self.offense,
            weights=[p.shot_accuracy ** SHOOTING_TENDENCY_FACTOR for p in self.offense],
            k=1
        )[0] # Better players shoot more

        points: int = 0

        if random.random() < player.shot_accuracy:
            points += 2

        return player, points


    def print_score(self) -> str:
        team1_score_string: str = f"{BOLD if self.most_recent_scorer == 1 else ''}{self.team1_score:}{END}"
        team2_score_string: str = f"{BOLD if self.most_recent_scorer == 2 else ''}{self.team2_score:}{END}"
        return f"{team1_score_string} - {team2_score_string}"


    def rebound(self) -> Player:
        players: list[Player] = (
            self.offense + self.defense
        )

        weights: list[float] = (
            [p.rebounding * OFFENSIVE_REBOUNDING_FACTOR for p in self.offense] +
            [p.rebounding * DEFENSIVE_REBOUNDING_FACTOR for p in self.defense]
        )

        return random.choices(players, weights=weights, k=1)[0]


    @staticmethod
    def print_time(period_time) -> str:
        return f"{period_time // 60 :02}:{period_time % 60 :02}"
