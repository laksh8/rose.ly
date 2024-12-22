import sqlite3
from rich.console import Console
from rich.table import Table

def view_progress():
    """Display progress for all habits."""
    conn = sqlite3.connect("data/habits.db")
    c = conn.cursor()
    c.execute("SELECT name, points FROM habits")
    rows = c.fetchall()

    console = Console()
    table = Table(title="\nrose.ly\n")
    table.add_column("Habit", style="cyan")
    table.add_column("Points", style="green")

    for name, points in rows:
        table.add_row(name, str(points))

    console.print(table)
    console.print('\n')
    conn.close()
