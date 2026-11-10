
import csv

from src.models import Team, Fixture


def load_teams(file_path):
    teams = {}

    with open(file_path, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required_fields = {"team_id", "name", "elo"}

        if not required_fields.issubset(reader.fieldnames or []):
            raise ValueError(
                f"CSV file must contain the following fields: {required_fields}"
            )

        for row in reader:
            team_id = int(row["team_id"])
            name = row["name"].strip()
            elo = float(row["elo"])

            if team_id in teams:
                raise ValueError(f"Duplicate team_id found: {team_id}")

            if not name:
                raise ValueError(f"Team name cannot be empty for team_id: {team_id}")

            teams[team_id] = Team(
                team_id=team_id,
                name=name,
                elo=elo
            )

    return teams

def load_fixtures(file_path, teams):
    fixtures = []       
    fixture_ids = set()

    with open(file_path, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        
        required_fields = {
            "fixture_id", 
            "matchday", 
            "date", 
            "home_team_id", 
            "away_team_id", 
            "status", 
            "home_goals", 
            "away_goals"
            }
        
        if not required_fields.issubset(reader.fieldnames or []):
            raise ValueError(
                f"CSV file must contain the following fields: {required_fields}"
            )
        for row in reader:
            fixture_id = int(row["fixture_id"])
            matchday = int(row["matchday"])
            date = (row["date"] or "").strip()

            home_id = int(row["home_team_id"])
            away_id = int(row["away_team_id"])

            status = (row["status"] or "").strip().upper()

            home_score = (row["home_goals"] or "").strip()
            away_score = (row["away_goals"] or "").strip()


            if fixture_id in fixture_ids:
                raise ValueError(f"Duplicate fixture_id found: {fixture_id}")
            
            fixture_ids.add(fixture_id)

            if home_id not in teams or away_id not in teams:
                raise ValueError(f"Fixture {fixture_id} references unknown team IDs: {home_id}, {away_id}")

            if home_id == away_id:
                raise ValueError(f"Fixture {fixture_id} has the same team playing against itself: {home_id}")

            if matchday < 1 or matchday > 6:
                raise ValueError(f"Fixture {fixture_id} has an invalid matchday: {matchday}")

            if not date or not status:
                raise ValueError(f"Fixture {fixture_id} has missing date or status")

            if bool(home_score) != bool(away_score):
                raise ValueError(f"Fixture {fixture_id} has inconsistent score data: home_goals={home_score}, away_goals={away_score}")
            
            home_goals = int(home_score) if home_score else None
            away_goals = int(away_score) if away_score else None

            if home_goals is not None and (home_goals < 0 or away_goals < 0):
                raise ValueError(f"Invalid score in fixture {fixture_id}")

            fixture = Fixture(
                fixture_id=fixture_id,
                matchday=matchday,
                date=date,
                home_team_id=home_id,
                away_team_id=away_id,
                status=status,
                home_goals=home_goals,
                away_goals=away_goals
            )

            fixtures.append(fixture)
            
    return fixtures