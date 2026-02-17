# Game management constants
PLAYERS_ON_COURT: int = 5
REGULATION_PERIODS: int = 4
REGULATION_PERIOD_LENGTH: int = 12 * 60
OVERTIME_PERIOD_LENGTH: int = 5 * 60
SHOT_CLOCK_LENGTH: int = 24
MIN_REBOUND_TIME: int = 0
MAX_REBOUND_TIME: int = 2

if REGULATION_PERIODS < 1: raise ValueError("Periods must be >= 1")
if REGULATION_PERIOD_LENGTH < 1: raise ValueError("Period length must be >= 1")
if OVERTIME_PERIOD_LENGTH < 1: raise ValueError("Overtime length must be >= 1")
if SHOT_CLOCK_LENGTH < 1: raise ValueError("Shot clock must be >= 1")
if SHOT_CLOCK_LENGTH > REGULATION_PERIOD_LENGTH: raise ValueError("Shot clock must be <= period seconds")
if SHOT_CLOCK_LENGTH > OVERTIME_PERIOD_LENGTH: raise ValueError("Shot clock must be <= overtime seconds")
if MIN_REBOUND_TIME < 0: raise ValueError("Minimum rebound time must be >= 0")
if MAX_REBOUND_TIME <= MIN_REBOUND_TIME: raise ValueError("Maximum rebound time must be > minimum rebound time")

# Game simulation constants
OFFENSIVE_REBOUNDING_FACTOR = 0.3 # 0 = no offensive rebounds, 1 = only offensive rebounds
DEFENSIVE_REBOUNDING_FACTOR = 1 - OFFENSIVE_REBOUNDING_FACTOR

if OFFENSIVE_REBOUNDING_FACTOR > 1: raise ValueError("Offensive rebounding factor must be <= 1")
if OFFENSIVE_REBOUNDING_FACTOR < 0: raise ValueError("Offensive rebounding factor must be >= 0")

# Player constants
SHOOTING_EFFICIENCY_MEAN: float = 0.5
SHOOTING_EFFICIENCY_SD: float = 0.15
REBOUNDING_MEAN: float = 0.5
REBOUNDING_SD: float = 0.15
DEFENSE_MEAN: float = 0.5
DEFENSE_SD: float = 0.15
SHOOTING_TENDENCY_FACTOR: float = 0.75 # Higher means better shooters shoot more shots
DEFENSE_IMPACT_FACTOR: float = 1 # Higher means defense affects efficiency more

if SHOOTING_EFFICIENCY_MEAN > 1: raise ValueError("Mean must be <= 1")
if SHOOTING_EFFICIENCY_SD < 0: raise ValueError("Mean must be >= 0")
if REBOUNDING_MEAN > 1: raise ValueError("Mean must be <= 1")
if REBOUNDING_SD < 0: raise ValueError("Mean must be >= 0")
if DEFENSE_MEAN > 1: raise ValueError("Mean must be <= 1")
if DEFENSE_MEAN < 0: raise ValueError("Mean must be >= 0")
if DEFENSE_SD < 0: raise ValueError("Mean must be >= 0")
if DEFENSE_SD > 1: raise ValueError("Mean must be <= 1")
if SHOOTING_TENDENCY_FACTOR < 0: raise ValueError("Tendency factor must be >= 0")

# Printing constants
USE_COLORS = False # Only when printing to terminal

if USE_COLORS:
    BLUE = '\033[94m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'
else:
    BLUE = ''
    RED = ''
    BOLD = ''
    END = ''

from enum import Enum, auto

# Display event types
class Event(Enum):
    REGULATION_PERIOD = auto()
    OVERTIME_PERIOD = auto()
    TIME_DISPLAY = auto()
    SCORE_DISPLAY = auto()
    SHOT_ATTEMPT = auto()
    REBOUND = auto()
    WINNER = auto()
    BOXSCORE = auto()

PLAY_EVENTS = [Event.SHOT_ATTEMPT, Event.REBOUND]
PERIOD_EVENTS = [Event.REGULATION_PERIOD, Event.OVERTIME_PERIOD]

