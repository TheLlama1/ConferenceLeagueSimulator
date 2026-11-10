
from dataclasses import dataclass


@dataclass
class Record:
    team_id: int

    played: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0

    goals_for: int = 0
    goals_against: int = 0

    away_goals: int = 0
    away_wins: int = 0

    points: int = 0

    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against

    def add_result(self, goals_for, goals_against, away=False):

        self.played += 1

        self.goals_for += goals_for
        self.goals_against += goals_against

        if away:
            self.away_goals += goals_for

        if goals_for > goals_against:

            self.wins += 1
            self.points += 3

            if away:
                self.away_wins += 1

        elif goals_for == goals_against:

            self.draws += 1
            self.points += 1

        else:
            self.losses += 1


def calculate_standings(teams, fixtures):

    table = {
        team_id: Record(team_id)
        for team_id in teams
    }

    for fixture in fixtures:

        if not fixture.played:
            continue

        home_id = fixture.home_team_id
        away_id = fixture.away_team_id

        home_goals = fixture.home_goals
        away_goals = fixture.away_goals

        table[home_id].add_result(
            home_goals,
            away_goals
        )

        table[away_id].add_result(
            away_goals,
            home_goals,
            away=True
        )

    def ranking_key(record):

        return (
            -record.points,
            -record.goal_difference,
            -record.goals_for,
            -record.away_goals,
            -record.wins,
            -record.away_wins,
            teams[record.team_id].name.casefold()
        )

    standings = sorted(
        table.values(),
        key=ranking_key
    )

    return standings
