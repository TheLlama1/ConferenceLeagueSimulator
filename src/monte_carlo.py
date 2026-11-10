
from dataclasses import replace

from src.standings import calculate_standings
from src.match_simulator import MatchSimulator


def simulate_season(teams, fixtures, simulator):
    simulated_fixtures = []

    for fixture in fixtures:
        if fixture.played:
            simulated_fixtures.append(fixture)
            continue

        home_team = teams[fixture.home_team_id]
        away_team = teams[fixture.away_team_id]

        home_goals, away_goals = simulator.simulate_score(
            home_team,
            away_team
        )

        simulated_fixtures.append(
            replace(
                fixture,
                status="FT",
                home_goals=home_goals,
                away_goals=away_goals
            )
        )

    return calculate_standings(teams, simulated_fixtures)


def run_monte_carlo(teams, fixtures, iterations=10000, seed=None):

    if iterations <= 0:
        raise ValueError("Iterations must be greater than zero.")

    simulator = MatchSimulator(seed=seed)

    results = {
        team_id: {
            "first_place": 0,
            "top_8": 0,
            "playoffs": 0,
            "eliminated": 0,
            "last_place": 0,
            "total_position": 0
        }
        for team_id in teams
    }

    for _ in range(iterations):

        standings = simulate_season(
            teams,
            fixtures,
            simulator
        )

        for position, record in enumerate(standings, start=1):

            team_result = results[record.team_id]

            if position == 1:
                team_result["first_place"] += 1

            if position <= 8:
                team_result["top_8"] += 1

            elif position <= 24:
                team_result["playoffs"] += 1

            else:
                team_result["eliminated"] += 1

            if position == len(standings):
                team_result["last_place"] += 1

            team_result["total_position"] += position

    for team_result in results.values():

        percentage_fields = (
            "first_place",
            "top_8",
            "playoffs",
            "eliminated",
            "last_place"
        )

        for field in percentage_fields:
            team_result[field] = (
                team_result[field] / iterations * 100
            )

        team_result["average_position"] = (
            team_result["total_position"] / iterations
        )

        del team_result["total_position"]

    return results
