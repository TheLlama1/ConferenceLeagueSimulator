from pathlib import Path

from src.data_loader import load_teams, load_fixtures
from src.match_simulator import MatchSimulator
from src.monte_carlo import simulate_season
from src.knockout import (
    draw_playoff_ties,
    simulate_knockout_round,
    draw_round_of_16,
    draw_quarter_finals,
    draw_semi_finals,
    simulate_final,
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


# STEP 6: Draw the quarter-finals.
quarter_final_ties = draw_quarter_finals(
    teams,
    r16_ties,
    r16_results
)

print("\n" + "=" * 65)
print("                  QUARTER-FINAL DRAW")
print("=" * 65)

for tie in quarter_final_ties:
    print(f"\n{tie.tie_id}")

    print(
        f"First leg:  "
        f"{teams[tie.first_leg_home_id].name} (HOME) vs "
        f"{teams[tie.second_leg_home_id].name}"
    )

    print(
        f"Second leg: "
        f"{teams[tie.second_leg_home_id].name} (HOME) vs "
        f"{teams[tie.first_leg_home_id].name}"
    )


# STEP 7: Simulate the quarter-finals.
quarter_final_results = simulate_knockout_round(
    teams,
    quarter_final_ties,
    simulator
)

print("\n" + "=" * 65)
print("                  SEMI-FINALISTS")
print("=" * 65)

for tie in quarter_final_ties:
    result = quarter_final_results[tie.tie_id]
    winner = teams[result.winner_id]

    print(
        f"{tie.tie_id}: {winner.name} "
        f"(Decided by: {result.decided_by})"
    )

print("\nQualified teams:", len(quarter_final_results))


# STEP 8: Draw the semi-finals.
semi_final_ties = draw_semi_finals(
    teams,
    quarter_final_ties,
    quarter_final_results
)

print("\n" + "=" * 65)
print("                   SEMI-FINAL DRAW")
print("=" * 65)

for tie in semi_final_ties:
    print(f"\n{tie.tie_id}")

    print(
        f"First leg:  "
        f"{teams[tie.first_leg_home_id].name} (HOME) vs "
        f"{teams[tie.second_leg_home_id].name}"
    )

    print(
        f"Second leg: "
        f"{teams[tie.second_leg_home_id].name} (HOME) vs "
        f"{teams[tie.first_leg_home_id].name}"
    )


# STEP 9: Simulate the semi-finals.
semi_final_results = simulate_knockout_round(
    teams,
    semi_final_ties,
    simulator
)

print("\n" + "=" * 65)
print("                    FINALISTS")
print("=" * 65)

finalists = []

for tie in semi_final_ties:
    result = semi_final_results[tie.tie_id]
    winner = teams[result.winner_id]

    finalists.append(winner.team_id)

    print(
        f"{tie.tie_id}: {winner.name} "
        f"(Decided by: {result.decided_by})"
    )

print("\nQualified teams:", len(finalists))

# STEP 10: Simulate the final.
final_result = simulate_final(
    teams,
    finalists,
    simulator
)

team1 = teams[final_result.team1_id]
team2 = teams[final_result.team2_id]

print("\n" + "=" * 65)
print("              UEFA CONFERENCE LEAGUE FINAL")
print("=" * 65)

print(f"\n{team1.name} vs {team2.name}")

print("\n90 minutes:")
print(
    f"{team1.name} {final_result.team1_goals} - "
    f"{final_result.team2_goals} {team2.name}"
)

if final_result.decided_by in ("Extra time", "Penalties"):
    print("\nExtra time:")
    print(
        f"{team1.name} {final_result.extra_time_team1_goals} - "
        f"{final_result.extra_time_team2_goals} {team2.name}"
    )

if final_result.decided_by == "Penalties":
    print("\nPenalty shootout:")
    print(
        f"{team1.name} {final_result.penalties_team1} - "
        f"{final_result.penalties_team2} {team2.name}"
    )

champion = teams[final_result.winner_id]

print("\n" + "=" * 65)
print("                  TOURNAMENT CHAMPION")
print("=" * 65)

print(f"\n             🏆 {champion.name.upper()} 🏆")
print(f"\nDecided by: {final_result.decided_by}")
print("=" * 65)
