
def display_qualification_report(teams, results):

    ranked_teams = sorted(
        results.items(),
        key=lambda item: (
            item[1]["average_position"],
            -item[1]["top_8"]
        )
    )

    print("\n" + "=" * 105)
    print("             UEFA CONFERENCE LEAGUE - MONTE CARLO PROJECTIONS")
    print("=" * 105)

    print(
        f"{'Team':<25}"
        f"{'Avg Pos':>9}"
        f"{'1st':>9}"
        f"{'Top 8':>9}"
        f"{'Playoffs':>11}"
        f"{'Out':>9}"
        f"{'Last':>9}"
    )

    print("-" * 105)

    for team_id, result in ranked_teams:

        team = teams[team_id]

        print(
            f"{team.name:<25}"
            f"{result['average_position']:>9.2f}"
            f"{result['first_place']:>8.1f}%"
            f"{result['top_8']:>8.1f}%"
            f"{result['playoffs']:>10.1f}%"
            f"{result['eliminated']:>8.1f}%"
            f"{result['last_place']:>8.1f}%"
        )

    print("=" * 105)
