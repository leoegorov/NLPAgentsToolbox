#!/usr/bin/env python3
import requests # type: ignore
import random
import sqlite3
import os
import sys
import argparse

# fallback variables
DATABASE_FILE = os.environ.get('DATABASE_FILE', 'juror.db')
API_CENSUS  = os.environ.get('API_CENSUS', 'https://api.census.gov/data/2020/dec/pl')
# API_KEY = None  # Optional: Replace with your key like 'your_api_key_here'

def check_environment_variables():
    if 'DATABASE_FILE' not in os.environ:
        print(f"Warning: DATABASE_FILE location is not set. Defaulting to {os.getcwd()}/{DATABASE_FILE}", file=sys.stderr)

# Get list of U.S. states and populations
def fetch_state_populations():
    params = {
        'get': 'NAME,P1_001N',
        'for': 'state:*'
    }
    # if API_KEY:
    #     params['key'] = API_KEY

    response = requests.get(API_CENSUS, params=params)
    data = response.json()
    headers, rows = data[0], data[1:]
    return [(row[0], int(row[1]), row[2]) for row in rows]  # (state_name, population, state_code)

# Select a random state based on population
def select_state_weighted(states):
    names = [s[0] for s in states]
    weights = [s[1] for s in states]
    chosen_index = random.choices(range(len(states)), weights=weights)[0]
    return states[chosen_index]

# Generate random age and gender
def generate_random_person():
    age = random.randint(0, 100)  # Assume age 0 to 100
    gender = random.choice(['Male', 'Female'])
    return age, gender

# Initialize and write to SQLite
def save_person_to_db(age, gender, state):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            gender TEXT,
            state TEXT
        )
    ''')
    cur.execute('INSERT INTO person (age, gender, state) VALUES (?, ?, ?)', (age, gender, state))
    conn.commit()
    conn.close()

def main():
    parser = argparse.ArgumentParser(
        description='mkbio – create an American and call make them a juror'
    )
    parser.add_argument('--version', action='version', version='mkbio v0.0')
    args = parser.parse_args()

    check_environment_variables()
    print("Fetching U.S. population data by state...")
    states = fetch_state_populations()
    state_name, _, _ = select_state_weighted(states)
    age, gender = generate_random_person()
    save_person_to_db(age, gender, state_name)
    print(f"Installed as juror: Age={age}, Gender={gender}, State={state_name}")

if __name__ == '__main__':
    main()