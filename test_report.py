
from pathlib import Path

from src.data_loader import load_teams
from src.models import Fixture
from src.monte_carlo import run_monte_carlo
from src.report import display_qualification_report


ROOT = Path(__file__).resolve().parent

teams = load_teams(ROOT / "data" / "team_ratings.csv")

test_fixtures = [
    Fixture(1, 1, "TEST", 2, 3, "NS"),
    Fixture(2, 1, "TEST", 3, 1, "NS"),
    Fixture(3, 1, "TEST", 2, 1, "NS")
]

results = run_monte_carlo(
    teams,
    test_fixtures,
    iterations=1000,
    seed=42
)

display_qualification_report(teams, results)
