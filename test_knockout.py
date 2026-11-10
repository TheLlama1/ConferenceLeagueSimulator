
from pathlib import Path

from src.data_loader import load_teams, load_fixtures
from src.match_simulator import MatchSimulator
from src.monte_carlo import simulate_season
from src.knockout import draw_playoff_ties, display_playoff_draw


ROOT = Path(__file__).resolve().parent

teams = load_teams(ROOT / "data" / "team_ratings.csv")

fixtures = load_fixtures(
    ROOT / "data" / "fixtures.csv",
    teams
)

simulator = MatchSimulator(seed=42)

# Simulate one complete league phase.
standings = simulate_season(
    teams,
    fixtures,
    simulator
)

# Draw the knockout play-offs.
ties = draw_playoff_ties(
    teams,
    standings,
    seed=42
)

display_playoff_draw(teams, ties)
