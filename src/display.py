
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()


def show_header():
    console.clear()
    console.print(
        Panel(
            "[bold white]UEFA CONFERENCE LEAGUE[/bold white]\n"
            "[bright_red]TOURNAMENT SIMULATOR[/bright_red]",
            border_style="bright_red",
            padding=(1, 4),
            expand=False
        ),
        justify="center"
    )


def show_section(title):
    console.print()
    console.rule(f"[bold cyan]{title}[/bold cyan]")
    console.print()


def show_league_table(teams, standings):
    table = Table(
        title="LEAGUE PHASE FINAL STANDINGS",
        box=box.ROUNDED,
        show_lines=False
    )

    table.add_column("Pos", justify="center")
    table.add_column("Team", min_width=25)
    table.add_column("P", justify="center")
    table.add_column("W", justify="center")
    table.add_column("D", justify="center")
    table.add_column("L", justify="center")
    table.add_column("GD", justify="center")
    table.add_column("Pts", justify="center", style="bold")

    for index, record in enumerate(standings):
        team_id = record.team_id
        team = teams[team_id]

        if index < 8:
            style = "green"
        elif index < 24:
            style = "yellow"
        else:
            style = "dim"

        table.add_row(
            str(index + 1),
            team.name,
            str(record.played),
            str(record.wins),
            str(record.draws),
            str(record.losses),
            str(record.goal_difference),
            str(record.points),
            style=style
        )

    console.print(table)
    console.print("[green]Positions 1–8: Direct qualification[/green]")
    console.print("[yellow]Positions 9–24: Knockout play-offs[/yellow]")
    console.print("[dim]Positions 25–36: Eliminated[/dim]")


def show_knockout_draw(teams, ties, title):
    show_section(title)

    for tie in ties:
        first_home = teams[tie.first_leg_home_id]
        second_home = teams[tie.second_leg_home_id]

        console.print(
            Panel(
                f"[bold]{first_home.name}[/bold] vs [bold]{second_home.name}[/bold]\n"
                "[dim]Two-legged tie[/dim]",
                border_style="blue",
                expand=False
            )
        )


def show_knockout_results(teams, ties, results, title):
    show_section(title)

    for tie in ties:
        result = results[tie.tie_id]

        first_home = teams[tie.first_leg_home_id]
        first_away = teams[tie.second_leg_home_id]

        details = (
            f"First leg: {first_home.name} "
            f"[bold]{result.first_leg_home_goals} - "
            f"{result.first_leg_away_goals}[/bold] {first_away.name}\n"
            f"Second leg: {first_away.name} "
            f"[bold]{result.second_leg_home_goals} - "
            f"{result.second_leg_away_goals}[/bold] {first_home.name}\n"
            f"Aggregate: [bold]{result.aggregate_home} - "
            f"{result.aggregate_away}[/bold]\n"
        )

        if result.decided_by == "extra_time":
            details += "[yellow]Decided after extra time[/yellow]\n"
        elif result.decided_by == "penalties":
            details += (
                f"[yellow]Decided on penalties: "
                f"{result.penalties_home} - {result.penalties_away}[/yellow]\n"
            )

        winner = teams[result.winner_id]
        details += f"\n[bold green]Qualified: {winner.name}[/bold green]"

        console.print(Panel(details, border_style="green"))


def show_final(teams, result):
    show_section("UEFA CONFERENCE LEAGUE FINAL")

    team1 = teams[result.team1_id]
    team2 = teams[result.team2_id]

    details = (
        f"[bold]{team1.name}[/bold] "
        f"[bold cyan]{result.team1_goals} - {result.team2_goals}[/bold cyan] "
        f"[bold]{team2.name}[/bold]"
    )

    if result.decided_by == "extra_time":
        details += "\n[yellow]Decided after extra time[/yellow]"
    elif result.decided_by == "penalties":
        details += (
            f"\n[yellow]Penalties: {result.penalties_team1} - "
            f"{result.penalties_team2}[/yellow]"
        )

    details += (
        f"\n\n[bold gold1]CHAMPIONS: "
        f"{teams[result.winner_id].name.upper()}[/bold gold1]"
    )

    console.print(
        Panel(
            details,
            border_style="gold1",
            padding=(1, 3),
            expand=False
        ),
        justify="center"
    )
