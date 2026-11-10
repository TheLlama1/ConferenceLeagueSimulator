
from pathlib import Path

from src.data_loader import load_teams, load_fixtures
from src.standings import calculate_standings
from src.validation import validate_league_phase


ROOT = Path(__file__).resolve().parent

teams = load_teams(ROOT / "data" / "team_ratings.csv")
fixtures = load_fixtures(ROOT / "data" / "fixtures.csv", teams)

if not validate_league_phase(teams, fixtures):
    raise SystemExit("Please fix the fixture data first.")

standings = calculate_standings(teams, fixtures)

print("\nCURRENT CONFERENCE LEAGUE TABLE")

print(
    f"{'Pos':>3} {'Team':<25} "
    f"{'P':>2} {'W':>2} {'D':>2} {'L':>2} "
    f"{'GF':>3} {'GA':>3} {'GD':>4} {'Pts':>3}"
)

for position, record in enumerate(standings, 1):
    team = teams[record.team_id]

    print(
        f"{position:>3} "
        f"{team.name:<25} "
        f"{record.played:>2} "
        f"{record.wins:>2} "
        f"{record.draws:>2} "
        f"{record.losses:>2} "
        f"{record.goals_for:>3} "
        f"{record.goals_against:>3} "
        f"{record.goal_difference:>+4} "
        f"{record.points:>3}"
    )
