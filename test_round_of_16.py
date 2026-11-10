from pathlib import Path

from src.data_loader import load_teams, load_fixtures
from src.match_simulator import MatchSimulator
from src.monte_carlo import simulate_season
from src.knockout import (
    draw_playoff_ties,
    simulate_knockout_round,
    draw_round_of_16,
    display_playoff_draw
)


ROOT = Path(__file__).resolve().parent

teams = load_teams(ROOT / "data" / "team_ratings.csv")
fixtures = load_fixtures(ROOT / "data" / "fixtures.csv", teams)

simulator = MatchSimulator(seed=42)

# STEP 1: Simulate the league phase.
standings = simulate_season(
    teams,
    fixtures,
    simulator
)

# STEP 2: Draw the play-offs.
playoff_ties = draw_playoff_ties(
    teams,
    standings,
    seed=42
)

display_playoff_draw(teams, playoff_ties)

# STEP 3: Simulate the play-offs.
playoff_results = simulate_knockout_round(
    teams,
    playoff_ties,
    simulator
)

# STEP 4: Draw the Round of 16.
r16_ties = draw_round_of_16(
    teams,
    standings,
    playoff_ties,
    playoff_results,
    seed=42
)

print("\n" + "=" * 65)
print("                  ROUND OF 16 DRAW")
print("=" * 65)

for tie in r16_ties:

    seeded = teams[tie.seeded_team_id]
    unseeded = teams[tie.unseeded_team_id]

    print(f"\n{tie.tie_id}")
    print(f"First leg:  {unseeded.name} (HOME) vs {seeded.name}")
    print(f"Second leg: {seeded.name} (HOME) vs {unseeded.name}")

# STEP 5: Simulate the Round of 16.
r16_results = simulate_knockout_round(
    teams,
    r16_ties,
    simulator
)

print("\n" + "=" * 65)
print("                 QUARTER-FINALISTS")
print("=" * 65)

quarter_finalists = []

for tie in r16_ties:

    result = r16_results[tie.tie_id]
    winner = teams[result.winner_id]

    quarter_finalists.append(winner.name)

    print(
        f"{tie.tie_id}: {winner.name} "
        f"(Decided by: {result.decided_by})"
    )

print("\nQualified teams:", len(quarter_finalists))
