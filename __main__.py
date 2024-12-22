from app.cli import app
from app.habits import init_db

if __name__ == "__main__":
    # Initialize the database
    init_db()
    # Start the CLI application
    app()
