
from pathlib import Path

from src.data_loader import load_teams
from src.knockout import (
    KnockoutTie,
    simulate_two_legged_tie
)
from src.match_simulator import MatchSimulator


ROOT = Path(__file__).resolve().parent

teams = load_teams(ROOT / "data" / "team_ratings.csv")

# Ajax vs Atalanta
tie = KnockoutTie(
    tie_id="TEST1",
    round_name="Knockout Play-offs",
    seeded_team_id=2,
    unseeded_team_id=3,
    first_leg_home_id=3,
    second_leg_home_id=2
)

simulator = MatchSimulator(seed=42)

result = simulate_two_legged_tie(
    teams,
    tie,
    simulator
)

print("\nTWO-LEGGED KNOCKOUT TEST")

home = teams[result.home_team_id]
away = teams[result.away_team_id]

print(f"\n{home.name} vs {away.name}")

print(
    f"First leg:  "
    f"{result.first_leg_home_goals}-"
    f"{result.first_leg_away_goals}"
)

print(
    f"Second leg: "
    f"{result.second_leg_away_goals}-"
    f"{result.second_leg_home_goals}"
)

print(
    f"\nAggregate: "
    f"{result.aggregate_home}-"
    f"{result.aggregate_away}"
)

if result.decided_by == "Extra time":
    print(
        f"Extra time: "
        f"{result.extra_time_away_goals}-"
        f"{result.extra_time_home_goals}"
    )

if result.decided_by == "Penalties":
    print(
        f"Penalties: "
        f"{result.penalties_home}-"
        f"{result.penalties_away}"
    )

winner = teams[result.winner_id]

print(f"\nWinner: {winner.name}")
print(f"Decided by: {result.decided_by}")
