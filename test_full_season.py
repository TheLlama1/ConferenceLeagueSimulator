
from pathlib import Path

from src.data_loader import load_teams, load_fixtures
from src.monte_carlo import run_monte_carlo
from src.report import display_qualification_report


ROOT = Path(__file__).resolve().parent

teams = load_teams(ROOT / "data" / "team_ratings.csv")

fixtures = load_fixtures(
    ROOT / "data" / "fixtures.csv",
    teams
)

results = run_monte_carlo(
    teams,
    fixtures,
    iterations=10000,
    seed=42
)

display_qualification_report(teams, results)
