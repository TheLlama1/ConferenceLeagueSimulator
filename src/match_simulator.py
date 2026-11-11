
import math
import random


class MatchSimulator:

    def __init__(
        self,
        home_advantage=60,
        average_total_goals=2.7,
        elo_scale=800,
        seed=None,
        average_goals=None
    ):
        # Support both names for the average goals setting.
        if average_goals is not None:
            average_total_goals = average_goals

        self.home_advantage = home_advantage
        self.average_total_goals = average_total_goals
        self.average_goals = average_total_goals
        self.elo_scale = elo_scale

        self.rng = random.Random(seed)

    def expected_goals(self, home, away, neutral=False):
        # Neutral matches have no home advantage.
        home_advantage = 0 if neutral else self.home_advantage

        difference = (
            home.elo
            + home_advantage
            - away.elo
        )

        ratio = 10 ** (difference / self.elo_scale)

        home_share = ratio / (1 + ratio)

        home_goals = self.average_total_goals * home_share
        away_goals = self.average_total_goals * (1 - home_share)

        return home_goals, away_goals

    def poisson_sample(self, expected_goals):
        if expected_goals < 0:
            raise ValueError("Expected goals must be non-negative.")

        limit = math.exp(-expected_goals)

        product = 1.0
        goals = 0

        while product > limit:
            goals += 1
            product *= self.rng.random()

        return goals - 1

    def simulate_score(self, home, away, neutral=False):
        home_expected, away_expected = self.expected_goals(
            home,
            away,
            neutral=neutral
        )

        home_score = self.poisson_sample(home_expected)
        away_score = self.poisson_sample(away_expected)

        return home_score, away_score

    @staticmethod
    def poisson_probability(goals, expected_goals):
        if goals < 0 or expected_goals < 0:
            raise ValueError(
                "Goals and expected goals must be non-negative."
            )

        return (
            math.exp(-expected_goals)
            * expected_goals ** goals
            / math.factorial(goals)
        )

    def probabilities(self, home, away, max_goals=12, neutral=False):
        if max_goals < 0:
            raise ValueError("max_goals cannot be negative.")

        home_expected, away_expected = self.expected_goals(
            home,
            away,
            neutral=neutral
        )

        home_win = 0.0
        draw = 0.0
        away_win = 0.0

        # Calculate probabilities for every possible scoreline.
        for home_goals in range(max_goals + 1):

            probability_home = self.poisson_probability(
                home_goals,
                home_expected
            )

            for away_goals in range(max_goals + 1):

                probability_away = self.poisson_probability(
                    away_goals,
                    away_expected
                )

                score_probability = (
                    probability_home * probability_away
                )

                if home_goals > away_goals:
                    home_win += score_probability

                elif home_goals == away_goals:
                    draw += score_probability

                else:
                    away_win += score_probability

        total = home_win + draw + away_win

        return {
            "home": home_win / total,
            "draw": draw / total,
            "away": away_win / total
        }

    @staticmethod
    def fair_odds(probabilities):
        odds = {}

        for outcome, probability in probabilities.items():
            if probability > 0:
                odds[outcome] = 1 / probability

        return odds
