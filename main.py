
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from src.data_loader import load_teams, load_fixtures
from src.match_simulator import MatchSimulator
from src.validation import validate_league_phase
from src.tournament import run_tournament


console = Console()


def show_menu():
    console.clear()

    console.print(
        Panel(
            "[bold white]UEFA CONFERENCE LEAGUE[/]\n"
            "[bright_red]TOURNAMENT SIMULATOR[/]\n\n"
            "[dim]2026/27 Season[/]",
            border_style="bright_red",
            padding=(1, 4)
        )
    )

    console.print("\n[bold]MAIN MENU[/]\n")

    console.print("[green]1.[/] Simulate one complete season")
    console.print("[cyan]2.[/] Simulate multiple seasons")
    console.print("[red]0.[/] Exit")

    return input("\nChoose an option: ").strip()


def single_season(teams, fixtures):
    simulator = MatchSimulator()

    run_tournament(
        teams,
        fixtures,
        simulator
    )

    input("\nPress Enter to return to the menu...")


def multiple_seasons(teams, fixtures):
    console.print("\n[bold]MULTIPLE SEASON SIMULATION[/]\n")

    try:
        iterations = int(
            input("How many seasons should be simulated? ")
        )

        if iterations <= 0:
            raise ValueError

    except ValueError:
        console.print("[red]Please enter a positive whole number.[/]")
        input("\nPress Enter to continue...")
        return

    simulator = MatchSimulator()

    championships = {team_id: 0 for team_id in teams}
    final_appearances = {team_id: 0 for team_id in teams}

    console.print(
        f"\nSimulating [bold cyan]{iterations:,}[/] tournaments..."
    )

    for iteration in range(iterations):
        result = run_tournament(
            teams,
            fixtures,
            simulator,
            display=False
        )

        champion_id = result["champion_id"]
        championships[champion_id] += 1

        for finalist_id in result["finalists"]:
            final_appearances[finalist_id] += 1

        if (iteration + 1) % max(1, iterations // 10) == 0:
            percentage = (iteration + 1) / iterations * 100
            console.print(
                f"[dim]Progress: {percentage:.0f}%[/]"
            )

    table = Table(
        title="TOURNAMENT PROBABILITIES",
        box=box.ROUNDED,
        border_style="bright_red"
    )

    table.add_column("#", justify="center")
    table.add_column("Team", min_width=25)
    table.add_column("Titles", justify="right")
    table.add_column("Win probability", justify="right")
    table.add_column("Final appearances", justify="right")

    ranked_teams = sorted(
        teams,
        key=lambda team_id: championships[team_id],
        reverse=True
    )

    for position, team_id in enumerate(ranked_teams, start=1):
        title_count = championships[team_id]
        win_probability = title_count / iterations * 100
        final_count = final_appearances[team_id]

        table.add_row(
            str(position),
            teams[team_id].name,
            str(title_count),
            f"{win_probability:.2f}%",
            f"{final_count / iterations * 100:.2f}%"
        )

    console.print()
    console.print(table)

    console.print(
        f"\n[dim]Completed {iterations:,} simulated tournaments.[/]"
    )

    input("\nPress Enter to return to the menu...")


def main():
    root = Path(__file__).resolve().parent

    teams = load_teams(
        root / "data" / "team_ratings.csv"
    )

    fixtures = load_fixtures(
        root / "data" / "fixtures.csv",
        teams
    )

    if not validate_league_phase(teams, fixtures):
        console.print("[red]League data validation failed.[/]")
        return

    while True:
        choice = show_menu()

        if choice == "1":
            single_season(teams, fixtures)

        elif choice == "2":
            multiple_seasons(teams, fixtures)

        elif choice == "0":
            console.print("\n[bold red]Goodbye![/]")
            break

        else:
            console.print("[red]Invalid option.[/]")
            input("Press Enter to try again...")


if __name__ == "__main__":
    main()
