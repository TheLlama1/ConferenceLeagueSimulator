
from collections import Counter


def validate_league_phase(teams, fixtures):

    errors = []

    if len(teams) != 36:
        errors.append(
            f"Expected 36 teams, found {len(teams)}."
        )

    if len(fixtures) != 108:
        errors.append(
            f"Expected 108 fixtures, found {len(fixtures)}."
        )

    appearances = Counter()
    home_matches = Counter()
    away_matches = Counter()
    matchdays = Counter()

    for fixture in fixtures:

        home_id = fixture.home_team_id
        away_id = fixture.away_team_id

        appearances[home_id] += 1
        appearances[away_id] += 1

        home_matches[home_id] += 1
        away_matches[away_id] += 1

        matchdays[fixture.matchday] += 1

    for team_id, team in teams.items():

        total = appearances[team_id]
        home = home_matches[team_id]
        away = away_matches[team_id]

        if total != 6:
            errors.append(
                f"{team.name}: expected 6 matches, found {total}."
            )

        if home != 3:
            errors.append(
                f"{team.name}: expected 3 home matches, found {home}."
            )

        if away != 3:
            errors.append(
                f"{team.name}: expected 3 away matches, found {away}."
            )

    for matchday in range(1, 7):

        count = matchdays[matchday]

        if count != 18:
            errors.append(
                f"Matchday {matchday}: expected 18 fixtures, found {count}."
            )

    if errors:
        print("\nLEAGUE PHASE VALIDATION FAILED")

        for error in errors:
            print(f"- {error}")

        return False

    print("\nLEAGUE PHASE VALIDATION PASSED")
    print("36 teams")
    print("108 fixtures")
    print("6 matches per team")
    print("3 home and 3 away matches per team")
    print("18 fixtures per matchday")

    return True
