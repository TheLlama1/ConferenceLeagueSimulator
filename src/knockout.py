from dataclasses import dataclass
import random

@dataclass
class KnockoutTie:
    tie_id: str
    round_name: str
    seeded_team_id: int
    unseeded_team_id: int
    first_leg_home_id: int
    second_leg_home_id: int
    bracket_position: int | None = None

def draw_playoff_ties(teams, standings, seed=None):
    if len(standings) != 36:
        raise ValueError("Standings must contain 36 teams.")

    rng = random.Random(seed)

    ranked_ids = [
        record.team_id
        for record in standings
    ]

    seeded_pairs = [
        (9, 10),
        (11, 12),
        (13, 14),
        (15, 16)
    ]

    unseeded_pairs = [
        (23, 24),
        (21, 22),
        (19, 20),
        (17, 18)
    ]

    ties = []
    tie_number = 1

    for seeded_positions, unseeded_positions in zip(
        seeded_pairs,
        unseeded_pairs
    ):

        seeded_teams = [
            ranked_ids[position - 1]
            for position in seeded_positions
        ]

        unseeded_teams = [
            ranked_ids[position - 1]
            for position in unseeded_positions
        ]

        rng.shuffle(seeded_teams)
        rng.shuffle(unseeded_teams)

        for seeded_id, unseeded_id in zip(
            seeded_teams,
            unseeded_teams
        ):

            if seeded_id not in teams or unseeded_id not in teams:
                raise ValueError(
                    "Unknown team in knockout draw."
                )

            tie = KnockoutTie(
                tie_id=f"PO{tie_number}",
                round_name="Knockout Playoffs",
                seeded_team_id=seeded_id,
                unseeded_team_id=unseeded_id,

                first_leg_home_id = unseeded_id,
                second_leg_home_id = seeded_id
            )

            ties.append(tie)
            tie_number += 1
    return ties

def display_playoff_draw(teams, ties):
    print("\n" + "=" * 65)
    print("             KNOCKOUT PHASE PLAY-OFF DRAW")
    print("=" * 65)

    for tie in ties:

        seeded = teams[tie.seeded_team_id]
        unseeded = teams[tie.unseeded_team_id]

        print(f"\n{tie.tie_id}")
        print(f"First leg:  {unseeded.name} (HOME) vs {seeded.name}")
        print(f"Second leg: {seeded.name} (HOME) vs {unseeded.name}")

    print("\n" + "=" * 65)

@dataclass
class KnockoutResult:
    tie_id: str

    first_leg_home_goals: int
    first_leg_away_goals: int

    second_leg_home_goals: int
    second_leg_away_goals: int

    aggregate_home: int
    aggregate_away: int

    extra_time_home_goals: int = 0
    extra_time_away_goals: int = 0

    penalties_home: int | None = None
    penalties_away: int | None = None

    winner_id: int | None = None
    decided_by: str = ""

    home_team_id: int = 0
    away_team_id: int = 0

    @property
    def penalties_home_goals(self):
        return self.penalties_home

    @penalties_home_goals.setter
    def penalties_home_goals(self, value):
        self.penalties_home = value

    @property
    def penalties_away_goals(self):
        return self.penalties_away

    @penalties_away_goals.setter
    def penalties_away_goals(self, value):
        self.penalties_away = value


@dataclass
class FinalResult:
    team1_id: int
    team2_id: int

    team1_goals: int
    team2_goals: int

    extra_time_team1_goals: int = 0
    extra_time_team2_goals: int = 0

    penalties_team1: int | None = None
    penalties_team2: int | None = None

    winner_id: int | None = None
    decided_by: str = ""

def simulate_penalty_shootout(home_team, away_team, rng):
    """
    Simulates a penalty shoot-out.

    Each team initially takes five penalties.
    If still level, the shoot-out continues in sudden death.
    """

    home_score = 0
    away_score = 0

    # First five penalties for each team.
    for round_number in range(5):

        if rng.random() < 0.75:
            home_score += 1

        if rng.random() < 0.75:
            away_score += 1

        home_remaining = 4 - round_number
        away_remaining = 4 - round_number

        if home_score > away_score + away_remaining:
            return home_team.team_id, home_score, away_score

        if away_score > home_score + home_remaining:
            return away_team.team_id, home_score, away_score

    # Sudden death: one penalty per team per round.
    while True:

        home_scored = rng.random() < 0.75
        away_scored = rng.random() < 0.75

        if home_scored:
            home_score += 1

        if away_scored:
            away_score += 1

        if home_scored and not away_scored:
            return home_team.team_id, home_score, away_score

        if away_scored and not home_scored:
            return away_team.team_id, home_score, away_score


def simulate_two_legged_tie(teams, tie, simulator):

    first_home = teams[tie.first_leg_home_id]
    first_away = teams[tie.second_leg_home_id]

    second_home = teams[tie.second_leg_home_id]
    second_away = teams[tie.first_leg_home_id]

    # FIRST LEG
    first_home_goals, first_away_goals = simulator.simulate_score(
        first_home,
        first_away
    )

    # SECOND LEG
    second_home_goals, second_away_goals = simulator.simulate_score(
        second_home,
        second_away
    )

    # Calculate aggregate scores.
    aggregate_home = first_home_goals + second_away_goals
    aggregate_away = first_away_goals + second_home_goals

    result = KnockoutResult(
        tie_id=tie.tie_id,

        first_leg_home_goals=first_home_goals,
        first_leg_away_goals=first_away_goals,

        second_leg_home_goals=second_home_goals,
        second_leg_away_goals=second_away_goals,

        home_team_id=first_home.team_id,
        away_team_id=first_away.team_id,

        aggregate_home=aggregate_home,
        aggregate_away=aggregate_away
    )

    # Determine the winner after 180 minutes.
    if aggregate_home > aggregate_away:
        result.winner_id = first_home.team_id
        result.decided_by = "Aggregate"

    elif aggregate_away > aggregate_home:
        result.winner_id = first_away.team_id
        result.decided_by = "Aggregate"

    else:
        # AGGREGATE DRAW: EXTRA TIME

        expected_home, expected_away = simulator.expected_goals(
            second_home,
            second_away
        )

        extra_home = simulator.poisson_sample(expected_home / 3)
        extra_away = simulator.poisson_sample(expected_away / 3)

        result.extra_time_home_goals = extra_home
        result.extra_time_away_goals = extra_away

        aggregate_home += extra_away
        aggregate_away += extra_home

        result.aggregate_home = aggregate_home
        result.aggregate_away = aggregate_away

        if aggregate_home > aggregate_away:
            result.winner_id = first_home.team_id
            result.decided_by = "Extra time"

        elif aggregate_away > aggregate_home:
            result.winner_id = first_away.team_id
            result.decided_by = "Extra time"

        else:
            # STILL DRAW: PENALTY SHOOT-OUT

            rng = simulator.rng

            winner_id, penalties_home, penalties_away = (
                simulate_penalty_shootout(
                    second_home,
                    second_away,
                    rng
                )
            )

            result.winner_id = winner_id
            result.penalties_home = penalties_home
            result.penalties_away = penalties_away
            result.decided_by = "Penalties"

    return result



def draw_round_of_16(teams, standings, playoff_ties, playoff_results, seed=None):
    if len(standings) != 36:
        raise ValueError("Expected standings for 36 teams.")

    if len(playoff_ties) != 8 or len(playoff_results) != 8:
        raise ValueError("Expected 8 play-off ties and results.")

    rng = random.Random(seed)

    ranked_ids = [record.team_id for record in standings]

    position_by_team = {
        team_id: position
        for position, team_id in enumerate(ranked_ids, start=1)
    }

    playoff_winners = {
        (9, 10): [],
        (11, 12): [],
        (13, 14): [],
        (15, 16): []
    }

    for tie in playoff_ties:
        result = playoff_results.get(tie.tie_id)

        if result is None or result.winner_id is None:
            raise ValueError(f"Missing winner for {tie.tie_id}")

        if result.winner_id not in (
            tie.seeded_team_id,
            tie.unseeded_team_id
        ):
            raise ValueError(f"Invalid winner in {tie.tie_id}")

        seeded_position = position_by_team.get(tie.seeded_team_id)

        if seeded_position is None:
            raise ValueError("Unknown seeded team.")

        if 9 <= seeded_position <= 10:
            group = (9, 10)
        elif 11 <= seeded_position <= 12:
            group = (11, 12)
        elif 13 <= seeded_position <= 14:
            group = (13, 14)
        elif 15 <= seeded_position <= 16:
            group = (15, 16)
        else:
            raise ValueError("Invalid seeded team in play-off tie.")

        playoff_winners[group].append(result.winner_id)

    # Each seeded pair is split across the two sides of the bracket.
    # The slot numbers determine the later quarter-final pairings.
    bracket_groups = [
        ((1, 2), (15, 16), (4, 8)),
        ((3, 4), (13, 14), (2, 6)),
        ((5, 6), (11, 12), (1, 5)),
        ((7, 8), (9, 10), (3, 7))
    ]

    round_of_16_ties = []

    for seeded_positions, playoff_group, slots in bracket_groups:
        seeded_teams = [
            ranked_ids[position - 1]
            for position in seeded_positions
        ]

        unseeded_teams = playoff_winners[playoff_group].copy()

        if len(unseeded_teams) != 2:
            raise ValueError(
                f"Expected 2 winners from group {playoff_group}."
            )

        rng.shuffle(seeded_teams)
        rng.shuffle(unseeded_teams)

        for slot, seeded_id, unseeded_id in zip(
            slots,
            seeded_teams,
            unseeded_teams
        ):
            if seeded_id not in teams or unseeded_id not in teams:
                raise ValueError("Unknown team in Round of 16 draw.")

            round_of_16_ties.append(
                KnockoutTie(
                    tie_id=f"R16-{slot}",
                    round_name="Round of 16",
                    seeded_team_id=seeded_id,
                    unseeded_team_id=unseeded_id,
                    first_leg_home_id=unseeded_id,
                    second_leg_home_id=seeded_id,
                    bracket_position=slot
                )
            )

    return round_of_16_ties




def simulate_knockout_round(teams, ties, simulator):

    results = {}

    for tie in ties:

        result = simulate_two_legged_tie(
            teams,
            tie,
            simulator
        )

        results[tie.tie_id] = result

    return results



def draw_quarter_finals(teams, r16_ties, r16_results):
    if len(r16_ties) != 8:
        raise ValueError("Expected exactly 8 Round of 16 ties.")

    winners_by_slot = {}

    for tie in r16_ties:
        slot = tie.bracket_position

        if slot is None or slot not in range(1, 9):
            raise ValueError(f"Invalid bracket position in {tie.tie_id}.")

        if slot in winners_by_slot:
            raise ValueError(f"Duplicate bracket position: {slot}")

        result = r16_results.get(tie.tie_id)

        if result is None or result.winner_id is None:
            raise ValueError(f"Missing winner for {tie.tie_id}")

        if result.winner_id not in (
            tie.seeded_team_id,
            tie.unseeded_team_id
        ):
            raise ValueError(f"Invalid winner in {tie.tie_id}")

        winners_by_slot[slot] = result.winner_id

    if set(winners_by_slot) != set(range(1, 9)):
        raise ValueError("Some Round of 16 positions are missing.")

    # Adjacent Round of 16 positions meet in each quarter-final.
    quarter_final_paths = [
        ("QF1", 1, 2),
        ("QF2", 3, 4),
        ("QF3", 5, 6),
        ("QF4", 7, 8)
    ]

    quarter_final_ties = []

    for position, (tie_id, first_slot, second_slot) in enumerate(
        quarter_final_paths,
        start=1
    ):
        first_team_id = winners_by_slot[first_slot]
        second_team_id = winners_by_slot[second_slot]

        quarter_final_ties.append(
            KnockoutTie(
                tie_id=tie_id,
                round_name="Quarter-finals",
                seeded_team_id=second_team_id,
                unseeded_team_id=first_team_id,
                first_leg_home_id=first_team_id,
                second_leg_home_id=second_team_id,
                bracket_position=position
            )
        )

    return quarter_final_ties

def draw_semi_finals(teams, quarter_final_ties, quarter_final_results):
    if len(quarter_final_ties) != 4:
        raise ValueError("Expected exactly 4 quarter-final ties.")

    winners = {}

    for tie in quarter_final_ties:
        result = quarter_final_results.get(tie.tie_id)

        if result is None or result.winner_id is None:
            raise ValueError(f"Missing winner for {tie.tie_id}")

        if result.winner_id not in (
            tie.seeded_team_id,
            tie.unseeded_team_id
        ):
            raise ValueError(f"Invalid winner in {tie.tie_id}")

        winners[tie.tie_id] = result.winner_id

    required_ties = {"QF1", "QF2", "QF3", "QF4"}

    if set(winners) != required_ties:
        raise ValueError("Quarter-final results are incomplete.")

    # QF2 and QF4 winners occupy the top-two bracket paths.
    semi_final_paths = [
        ("SF1", "QF1", "QF2"),
        ("SF2", "QF3", "QF4")
    ]

    semi_final_ties = []

    for position, (tie_id, first_path, second_path) in enumerate(
        semi_final_paths,
        start=1
    ):
        first_team_id = winners[first_path]
        second_team_id = winners[second_path]

        semi_final_ties.append(
            KnockoutTie(
                tie_id=tie_id,
                round_name="Semi-finals",
                seeded_team_id=second_team_id,
                unseeded_team_id=first_team_id,
                first_leg_home_id=first_team_id,
                second_leg_home_id=second_team_id,
                bracket_position=position
            )
        )

    return semi_final_ties


def simulate_final(teams, finalist_ids, simulator):
    if len(finalist_ids) != 2:
        raise ValueError("The final must have exactly 2 teams.")

    if finalist_ids[0] == finalist_ids[1]:
        raise ValueError("A team cannot play against itself.")

    if any(team_id not in teams for team_id in finalist_ids):
        raise ValueError("Unknown finalist.")

    team1 = teams[finalist_ids[0]]
    team2 = teams[finalist_ids[1]]

    team1_goals, team2_goals = simulator.simulate_score(
        team1,
        team2,
        neutral=True
    )

    result = FinalResult(
        team1_id=team1.team_id,
        team2_id=team2.team_id,
        team1_goals=team1_goals,
        team2_goals=team2_goals
    )

    if team1_goals == team2_goals:
        expected1, expected2 = simulator.expected_goals(
            team1,
            team2,
            neutral=True
        )

        extra1 = simulator.poisson_sample(expected1 / 3)
        extra2 = simulator.poisson_sample(expected2 / 3)

        result.extra_time_team1_goals = extra1
        result.extra_time_team2_goals = extra2

        team1_goals += extra1
        team2_goals += extra2

        if team1_goals > team2_goals:
            result.winner_id = team1.team_id
            result.decided_by = "Extra time"

        elif team2_goals > team1_goals:
            result.winner_id = team2.team_id
            result.decided_by = "Extra time"

        else:
            winner_id, penalties1, penalties2 = simulate_penalty_shootout(
                team1,
                team2,
                simulator.rng
            )

            result.winner_id = winner_id
            result.penalties_team1 = penalties1
            result.penalties_team2 = penalties2
            result.decided_by = "Penalties"

    else:
        if team1_goals > team2_goals:
            result.winner_id = team1.team_id
        else:
            result.winner_id = team2.team_id

        result.decided_by = "90 minutes"

    return result
