import os
import sqlite3

def init_db():
    os.makedirs("data", exist_ok=True)  # Create 'data' directory if it doesn't exist
    """Initialize the SQLite database and create tables."""
    conn = sqlite3.connect("data/habits.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
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


def delete_habit(habit: str):
    """Delete an existing habit in the database."""
    try:
        conn = sqlite3.connect("data/habits.db")
        c = conn.cursor()
        
        # Execute DELETE query
        c.execute("DELETE FROM habits WHERE name=?", (habit,))
        
        # Commit the changes to the database
        conn.commit()
        
        # Check if any row was affected (habit found and deleted)
        if c.rowcount == 0:
            print(f"No habit named '{habit}' found.")
        else:
            print(f"Habit '{habit}' deleted successfully.")
        
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        # Ensure connection is closed
        conn.close()



def check_in_habit(full_credit: bool, habit: str):
    """Mark a habit as completed for today."""
    conn = sqlite3.connect("data/habits.db")
    c = conn.cursor()
    c.execute("SELECT id, points FROM habits WHERE name = ?", (habit,))
    result = c.fetchone()
    if not result:
        print(f"Habit '{habit}' not found!")
        return

    habit_id, points = result
    from datetime import date
    today = date.today().isoformat()
    c.execute("SELECT * FROM logs WHERE habit_id = ? AND date = ?", (habit_id, today))
    if c.fetchone():
        print(f"Habit '{habit}' already checked in today!")
        return
    
    if full_credit:
        points += 10
    else:
        points += 5
    c.execute("UPDATE habits SET points = ? WHERE id = ?", (points, habit_id))
    c.execute("INSERT INTO logs (habit_id, date) VALUES (?, ?)", (habit_id, today))
    conn.commit()
    conn.close()
    print(f"Habit '{habit}' checked in! Points: {points}")
