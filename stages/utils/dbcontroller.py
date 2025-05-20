import os
import sqlite3
import sys

DATABASE_FILE = os.environ.get('DATABASE_FILE', 'juror.db')

def update_db(column, value, id=None):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    # Ensure the table exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS juror (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    ''')

    # Check if column exists
    cur.execute("PRAGMA table_info(juror)")
    columns = [row[1] for row in cur.fetchall()]
    if column not in columns:
        cur.execute(f'ALTER TABLE juror ADD COLUMN {column} TEXT')
        print(f"Created column {column}")

    # Determine id if not given
    if id is None:
        cur.execute('SELECT MAX(id) FROM juror')
        result = cur.fetchone()
        id = result[0]
        if id is None:
            # No entries exist yet; insert a new row first
            cur.execute('INSERT INTO juror DEFAULT VALUES')
            id = cur.lastrowid

    # Check if row with given id exists
    cur.execute('SELECT 1 FROM juror WHERE id = ?', (id,))
    if cur.fetchone() is None:
        cur.execute('INSERT INTO juror (id) VALUES (?)', (id,))

    # Update the value
    cur.execute(f'UPDATE juror SET {column} = ? WHERE id = ?', (value, id))

    conn.commit()
    conn.close()


# Get column value for highest or specified id
def get_val(column, id=None):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    # Determine id if not provided
    if id is None:
        cur.execute('SELECT MAX(id) FROM juror')
        result = cur.fetchone()
        if result is None or result[0] is None:
            conn.close()
            return None
        id = result[0]

    # Retrieve value
    try:
        cur.execute(f'SELECT {column} FROM juror WHERE id = ?', (id,))
        result = cur.fetchone()
        return result[0] if result else None
    except sqlite3.OperationalError:
        return None
    finally:
        conn.close()
