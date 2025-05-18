#!/usr/bin/env python3
import os
import sys
import re
import sqlite3
import importlib.util
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main():
    parser = argparse.ArgumentParser(description='mkbio – make some American jurors')
    parser.add_argument('-n', '--num', action='store', type=int, default=1, help='Amount of jurors to generate')
    parser.add_argument('--version', action='version', version='mkbio v0.0')
    args = parser.parse_args()

    # Global variables
    build_dir = os.environ.get('BUILD_DIR', 'build')
    # os.makedirs(build_dir, exist_ok=True)
    database_file = os.path.join(build_dir, 'juror.db')
    os.environ.setdefault('DATABASE_FILE', database_file)
    os.environ.setdefault('API_CENSUS', 'https://api.census.gov/data/2020/dec/pl')

    stages_dir = os.path.join(os.path.dirname(__file__), '..', 'stages')
    stages_dir = os.path.abspath(stages_dir)
    stage_files = []

    for filename in os.listdir(stages_dir):
        match = re.match(r'_([0-9]{2})-.*\.py$', filename)
        if match:
            stage_files.append((int(match.group(1)), filename))

    DATABASE_FILE = os.environ['DATABASE_FILE']

    for i in range(args.num):
        if args.num > 1:   print(f"\nCreating juror {i + 1} of {args.num}")

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
                print(f"\n\033[93mWarning: stages/{filename} has no main() function.\033[0m\n")

if __name__ == '__main__':
    main()