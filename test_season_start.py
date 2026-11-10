
from pathlib import Path

from src.data_loader import load_teams, load_fixtures


ROOT = Path(__file__).resolve().parent

teams = load_teams(ROOT / "data" / "team_ratings.csv")

fixtures = load_fixtures(
    ROOT / "data" / "fixtures.csv",
    teams
)

print("\nSEASON START CHECK")

print(f"Teams: {len(teams)}")
print(f"Fixtures: {len(fixtures)}")

print(
    "Played fixtures:",
    sum(fixture.played for fixture in fixtures)
)

print(
    "Unplayed fixtures:",
    sum(not fixture.played for fixture in fixtures)
)

print("\nFIRST FIVE FIXTURES")

for fixture in fixtures[:5]:

    home = teams[fixture.home_team_id]
    away = teams[fixture.away_team_id]

    print(
        f"MD{fixture.matchday}: "
        f"{home.name} vs {away.name} "
        f"({fixture.status})"
    )
