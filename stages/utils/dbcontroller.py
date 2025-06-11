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
        print(f"\033[93mCreated field {column}\033[0m")

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
        print(f"\033[93mError reading the database\033[0m")
        return None
    finally:
        conn.close()

    

def update_db_bio_quote( key_part, value_part):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    # Ensure the table exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS BIO_QUOTE (
            key_part TEXT NOT NULL PRIMARY KEY,
            value_part TEXT NOT NULL
        )
    ''')
    try:
        cur.execute("INSERT OR REPLACE INTO BIO_QUOTE (key_part, value_part) VALUES (?, ?)",
                       (key_part, value_part))
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        if conn:
            conn.close()

def select_bio_quote( search_key):
    """
    Selects and prints the value associated with a specific key_part.
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS BIO_QUOTE (
            key_part TEXT NOT NULL PRIMARY KEY,
            value_part TEXT NOT NULL
        )
        ''')
        
        # SQL query to select value_part where key_part matches search_key
        cursor.execute("SELECT value_part FROM BIO_QUOTE WHERE key_part = ?", (search_key,))
        result = cursor.fetchone() # fetchone() retrieves the first matching row

        if result:
            update_db_bio_quote( search_key, "other(-)")
            return result[0] # Return the value part
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error selecting key: {e}")
        return None
    finally:
        if conn:
            conn.close()
