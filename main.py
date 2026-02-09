import random

PLAYERS_ON_COURT: int = 2

class Player:
    def __init__(self, name: str):
        self.name = name
        self.shot_accuracy: float = random.normalvariate(0.5, 0.25)

    def __str__(self):
        return f"{self.name} ({self.shot_accuracy})"

    def __repr__(self):
        return self.__str__()

class Game:
    def __init__(self, team1: list[Player], team2: list[Player],
             quarters: int=4, quarter_seconds: int=12*60, shot_clock_seconds: int=24):
        assert quarters >= 1
        assert quarter_seconds >= 1
        assert quarter_seconds >= shot_clock_seconds >= 1
        assert len(team1) == PLAYERS_ON_COURT
        assert len(team2) == PLAYERS_ON_COURT

        self.team1 = team1
        self.team2 = team2
        self.quarters = quarters
        self.quarter_seconds = quarter_seconds
        self.shot_clock_seconds = shot_clock_seconds

    def sim_game(self) -> None:
        print(self.team1, self.team2)

        team1_ball: bool = True

        team1_score: int = 0
        team2_score: int = 0

        for quarter in range(self.quarters):
            print(f"Q{quarter + 1}")

            quarter_time: int = self.quarter_seconds

            while quarter_time > 0:
                time_elapsed, team1_score, team2_score = self.sim_possesion(quarter_time, team1_ball, team1_score, team2_score)
                quarter_time -= time_elapsed
                team1_ball = not team1_ball

                print(print_time(quarter_time))
                print(print_score(team1_score, team2_score))

    def sim_possesion(self, quarter_time: int, team1_ball: bool, team1_score: int, team2_score: int) -> (int, int, int):
        if quarter_time > self.shot_clock_seconds:
            time_elapsed = random.randrange(1, self.shot_clock_seconds)
        else:
            time_elapsed = quarter_time
        quarter_time -= time_elapsed
        if team1_ball:
            player, points = shot_attempt(self.team1)
            print(print_shot_attempts(player, points))
            team1_score += points
        else:
            player, points = shot_attempt(self.team2)
            print(print_shot_attempts(player, points))
            team2_score += points
        return (time_elapsed, team1_score, team2_score)


def shot_attempt(team: list[Player]) -> (Player, int):
    player: Player = random.choice(team)

    points: int = 0

    if random.random() < player.shot_accuracy:
        points += 2

    return player, points


def print_time(quarter_time) -> str:
    return f"{quarter_time // 60 :02}:{quarter_time % 60 :02}"


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