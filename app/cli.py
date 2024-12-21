import typer
from app.habits import add_habit, check_in_habit, delete_habit
from app.visualization import view_progress

app = typer.Typer()

@app.command()
def add(habit: str):
    """Add a new habit to track."""
    add_habit(habit)

@app.command()
def check_in(habit: str):
    """Mark a habit as completed."""
    check_in_habit(habit)

@app.command()
def progress():
    """View progress for all habits."""
    view_progress()


@app.command()
def delete(habit: str):
    """Delete an existing habit in the database."""
    delete_habit(habit)