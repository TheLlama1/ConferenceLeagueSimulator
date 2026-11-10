from dataclasses import dataclass

@dataclass
class Team:
    team_id: int
    name: str
    elo: float

@dataclass
class Fixture:
    fixture_id: int
    matchday: int
    date: str 
    home_team_id: int
    away_team_id: int
    status: str 
    home_goals: int | None = None
    away_goals: int | None = None

    @property
    def played(self):
        return self.home_goals is not None and self.away_goals is not None