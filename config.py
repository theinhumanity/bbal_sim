# Game constants
PLAYERS_ON_COURT: int = 3
REGULATION_PERIODS: int = 4
REGULATION_PERIOD_LENGTH: int = 12 * 60
OVERTIME_PERIOD_LENGTH: int = 5 * 60
SHOT_CLOCK_LENGTH: int = 24

if REGULATION_PERIODS < 1: raise ValueError("Periods must be >= 1")
if REGULATION_PERIOD_LENGTH < 1: raise ValueError("Period length must be >= 1")
if OVERTIME_PERIOD_LENGTH < 1: raise ValueError("Overtime length must be >= 1")
if SHOT_CLOCK_LENGTH < 1: raise ValueError("Shot clock must be >= 1")
if SHOT_CLOCK_LENGTH > REGULATION_PERIOD_LENGTH: raise ValueError("Shot clock must be <= period seconds")
if SHOT_CLOCK_LENGTH > OVERTIME_PERIOD_LENGTH: raise ValueError("Shot clock must be <= overtime seconds")

# Player constants
SHOOTING_EFFICIENCY_MEAN: float = 0.5
SHOOTING_EFFICIENCY_SD: float = 0.15

if SHOOTING_EFFICIENCY_MEAN > 1: raise ValueError("Mean must be <= 1")
if SHOOTING_EFFICIENCY_SD < 0: raise ValueError("Mean must be >= 0")