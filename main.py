#!/usr/bin/env python3
import os
import re
import sqlite3
import importlib.util

if __name__ == '__main__':

    # Set fallback variables
    os.environ.setdefault('DATABASE_FILE', 'build/juror.db')
    os.environ.setdefault('API_CENSUS', 'https://api.census.gov/data/2020/dec/pl')
    # API_KEY = None  # Optional: Replace with your key like 'your_api_key_here'

    stages_dir = os.path.join(os.path.dirname(__file__), 'stages')
    stage_files = []

    for filename in os.listdir(stages_dir):
        match = re.match(r'_([0-9]{2})-.*\.py$', filename)
        if match:
            stage_files.append((int(match.group(1)), filename))

    DATABASE_FILE = os.environ['DATABASE_FILE']

    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS person (id INTEGER PRIMARY KEY AUTOINCREMENT)')
    cur.execute('SELECT MAX(id) FROM person')
    result = cur.fetchone()
    new_id = (result[0] or 0) + 1
    cur.execute('INSERT INTO person (id) VALUES (?)', (new_id,))
    conn.commit()
    conn.close()

    for _, filename in sorted(stage_files):
        module_path = os.path.join(stages_dir, filename)
        module_name = os.path.splitext(filename)[0]

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        stage_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(stage_module)

        if hasattr(stage_module, 'main'):
            stage_module.main()
        else:
            print(f"\n\033[93mWarning: {filename} has no main() function.\033[0m")