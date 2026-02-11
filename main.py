import matplotlib.pyplot as plt

from displaygame import DisplayGame
from game import Game
from player import Player


def display_score_graph(game: Game) -> None:
    times = [t for t, _, _ in game.score_history]
    team1_scores = [s1 for _, s1, _ in game.score_history]
    team2_scores = [s2 for _, _, s2 in game.score_history]

    plt.plot(times, team1_scores, label="Team 1")
    plt.plot(times, team2_scores, label="Team 2")
    plt.xlabel("Game time (seconds)")
    plt.ylabel("Score")

    plt.show()

def main() -> None:
    team1: list[Player] = [Player('Kazuki'), Player('Adam'), Player('Rome'), Player('Sander'), Player('Zhenghan')]
    team2: list[Player] = [Player('Mauk'), Player('Jille'), Player('Jonah'), Player('Merlijn'), Player('Byuri')]

    game: Game = Game(team1, team2)

    game.sim_game()

    for event in game.event_list:
        print(event)

    display = DisplayGame()
    display.display_game(game)

    # display_score_graph(game)


if __name__ == '__main__':
    main()