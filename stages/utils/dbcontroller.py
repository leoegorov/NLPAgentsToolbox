import os
import sqlite3
import sys

DATABASE_FILE = os.environ.get('DATABASE_FILE', 'juror.db')

# def check_environment_variables():
#     if 'DATABASE_FILE' not in os.environ:
#         print(f"Warning: DATABASE_FILE location is not set. Defaulting to {os.getcwd()}/{DATABASE_FILE}", file=sys.stderr)

def update_db(column, value, id=None):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    # Ensure the table exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    ''')

    # Check if column exists
    cur.execute("PRAGMA table_info(person)")
    columns = [row[1] for row in cur.fetchall()]
    if column not in columns:
        cur.execute(f'ALTER TABLE person ADD COLUMN {column} TEXT')

    # Determine id if not given
    if id is None:
        cur.execute('SELECT MAX(id) FROM person')
        result = cur.fetchone()
        id = result[0]
        if id is None:
            # No entries exist yet; insert a new row first
            cur.execute('INSERT INTO person DEFAULT VALUES')
            id = cur.lastrowid

    # Check if row with given id exists
    cur.execute('SELECT 1 FROM person WHERE id = ?', (id,))
    if cur.fetchone() is None:
        cur.execute('INSERT INTO person (id) VALUES (?)', (id,))

    # Update the value
    cur.execute(f'UPDATE person SET {column} = ? WHERE id = ?', (value, id))

    conn.commit()
    conn.close()
