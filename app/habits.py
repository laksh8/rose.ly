import sqlite3

def init_db():
    """Initialize the SQLite database and create tables."""
    conn = sqlite3.connect("data/habits.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            streak INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            habit_id INTEGER,
            date TEXT,
            FOREIGN KEY(habit_id) REFERENCES habits(id)
        )
    """)
    conn.commit()
    conn.close()

def add_habit(habit: str):
    """Add a new habit to the database."""
    conn = sqlite3.connect("data/habits.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO habits (name) VALUES (?)", (habit,))
    conn.commit()
    conn.close()
    print(f"Habit '{habit}' added successfully!")

def check_in_habit(habit: str):
    """Mark a habit as completed for today."""
    conn = sqlite3.connect("data/habits.db")
    c = conn.cursor()
    c.execute("SELECT id, streak FROM habits WHERE name = ?", (habit,))
    result = c.fetchone()
    if not result:
        print(f"Habit '{habit}' not found!")
        return

    habit_id, streak = result
    from datetime import date
    today = date.today().isoformat()
    c.execute("SELECT * FROM logs WHERE habit_id = ? AND date = ?", (habit_id, today))
    if c.fetchone():
        print(f"Habit '{habit}' already checked in today!")
        return

    streak += 1
    points = streak * 10
    c.execute("UPDATE habits SET streak = ?, points = ? WHERE id = ?", (streak, points, habit_id))
    c.execute("INSERT INTO logs (habit_id, date) VALUES (?, ?)", (habit_id, today))
    conn.commit()
    conn.close()
    print(f"Habit '{habit}' checked in! Current streak: {streak}, Points: {points}")
