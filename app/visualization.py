import sqlite3
from rich.console import Console
from rich.table import Table

def view_progress():
    """Display progress for all habits."""
    conn = sqlite3.connect("data/habits.db")
    c = conn.cursor()
    c.execute("SELECT name, streak, points FROM habits")
    rows = c.fetchall()

    console = Console()
    table = Table(title="Habit Tracker Progress")
    table.add_column("Habit", style="cyan")
    table.add_column("Streak", style="green")
    table.add_column("Points", style="yellow")

    for name, streak, points in rows:
        table.add_row(name, str(streak), str(points))

    console.print(table)
    conn.close()
