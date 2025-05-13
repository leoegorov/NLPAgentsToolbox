import os
import sqlite3
import sys

DATABASE_FILE = os.environ.get('DATABASE_FILE', 'juror.db')

def check_environment_variables():
    if 'DATABASE_FILE' not in os.environ:
        print(f"Warning: DATABASE_FILE location is not set. Defaulting to {os.getcwd()}/{DATABASE_FILE}", file=sys.stderr)

def save_person_to_db(traits):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    #[gender, age, state_name, income, race, edu, occupation]
    cur.execute('''
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            gender TEXT,
            state TEXT,
            income TEXT,
            race TEXT,
            edu TEXT,
            occupation TEXT,
            first_name TEXT,
            last_name TEXT,
            religion TEXT
        )
    ''')
    cur.execute('INSERT INTO person (age, gender, state, income, race, edu, occupation,'
                ' first_name, last_name, religion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', traits)
    conn.commit()
    conn.close()
