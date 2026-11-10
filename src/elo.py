class EloSystem:
    def __init__(self, k_factor=20, home_advantage=60):
        self.k_factor = k_factor
        self.home_advantage = home_advantage

    def expected_score(self, home_elo, away_elo):

        difference = home_elo + self.home_advantage - away_elo

        expected_home = 1 / (1 + 10 ** (-difference / 400))

        return expected_home

    def update_elo(self,home_team,away_team,home_goals,away_goals):

        if home_goals > away_goals:
            actual_home = 1

        elif home_goals == away_goals:
            actual_home = 0.5
        else:
            actual_home = 0

        expected_home = self.expected_score(home_team.elo, away_team.elo)

        change = self.k_factor * (actual_home - expected_home)

        home_team.elo += change
        away_team.elo -= change

        return change