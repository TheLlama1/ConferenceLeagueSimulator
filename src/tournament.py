
from src.knockout import (
    draw_playoff_ties,
    simulate_knockout_round,
    draw_round_of_16,
    draw_quarter_finals,
    draw_semi_finals,
    simulate_final
)

from src.display import (
    show_header,
    show_section,
    show_league_table,
    show_knockout_draw,
    show_knockout_results,
    show_final
)

from src.monte_carlo import simulate_season


def run_tournament(teams, fixtures, simulator, seed=None, display=True):

    if display:
        show_header()
        show_section("SIMULATING LEAGUE PHASE")

    standings = simulate_season(
        teams,
        fixtures,
        simulator
    )

    if display:
        show_league_table(teams, standings)

    # KNOCKOUT PLAY-OFFS
    playoff_ties = draw_playoff_ties(
        teams,
        standings,
        seed=seed
    )

    if display:
        show_knockout_draw(
            teams,
            playoff_ties,
            "KNOCKOUT PLAY-OFF DRAW"
        )

    playoff_results = simulate_knockout_round(
        teams,
        playoff_ties,
        simulator
    )

    if display:
        show_knockout_results(
            teams,
            playoff_ties,
            playoff_results,
            "KNOCKOUT PLAY-OFF RESULTS"
        )

    # ROUND OF 16
    r16_ties = draw_round_of_16(
        teams,
        standings,
        playoff_ties,
        playoff_results,
        seed=seed
    )

    if display:
        show_knockout_draw(
            teams,
            r16_ties,
            "ROUND OF 16 DRAW"
        )

    r16_results = simulate_knockout_round(
        teams,
        r16_ties,
        simulator
    )

    if display:
        show_knockout_results(
            teams,
            r16_ties,
            r16_results,
            "ROUND OF 16 RESULTS"
        )

    # QUARTER-FINALS
    quarter_final_ties = draw_quarter_finals(
        teams,
        r16_ties,
        r16_results
    )

    if display:
        show_knockout_draw(
            teams,
            quarter_final_ties,
            "QUARTER-FINAL DRAW"
        )

    quarter_final_results = simulate_knockout_round(
        teams,
        quarter_final_ties,
        simulator
    )

    if display:
        show_knockout_results(
            teams,
            quarter_final_ties,
            quarter_final_results,
            "QUARTER-FINAL RESULTS"
        )

    # SEMI-FINALS
    semi_final_ties = draw_semi_finals(
        teams,
        quarter_final_ties,
        quarter_final_results
    )

    if display:
        show_knockout_draw(
            teams,
            semi_final_ties,
            "SEMI-FINAL DRAW"
        )

    semi_final_results = simulate_knockout_round(
        teams,
        semi_final_ties,
        simulator
    )

    if display:
        show_knockout_results(
            teams,
            semi_final_ties,
            semi_final_results,
            "SEMI-FINAL RESULTS"
        )

    finalists = [
        semi_final_results[tie.tie_id].winner_id
        for tie in semi_final_ties
    ]

    # FINAL
    final_result = simulate_final(
        teams,
        finalists,
        simulator
    )

    if display:
        show_final(teams, final_result)

    return {
        "standings": standings,
        "playoff_results": playoff_results,
        "round_of_16_results": r16_results,
        "quarter_final_results": quarter_final_results,
        "semi_final_results": semi_final_results,
        "finalists": finalists,
        "final_result": final_result,
        "champion_id": final_result.winner_id
    }
