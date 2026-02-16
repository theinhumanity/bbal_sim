from config import *

def format_time(seconds: int) -> str:
    return f"{seconds // 60 :02}:{seconds % 60 :02}"

def format_score(team1_score: int, team2_score: int, most_recent_scorer: int) -> str:
    team1_score_string: str = f"{BOLD if most_recent_scorer == 1 else ''}{team1_score:}{END}"
    team2_score_string: str = f"{BOLD if most_recent_scorer == 2 else ''}{team2_score:}{END}"
    return f"{team1_score_string} - {team2_score_string}"