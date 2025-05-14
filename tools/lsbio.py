#!/usr/bin/env python3
import sqlite3
import os
import sys
import argparse
import json

# Set fallback variables
os.environ.setdefault('DATABASE_FILE', 'build/juror.db')
DATABASE_FILE = os.environ['DATABASE_FILE']
os.environ.setdefault('EXPORT_FILE', 'build/export.json')
EXPORT_FILE = os.environ['EXPORT_FILE']

def check_environment_variables():
    if 'DATABASE_FILE' not in os.environ:
        print(f"Warning: DATABASE_FILE location is not set. Defaulting to {os.getcwd()}/{DATABASE_FILE}", file=sys.stderr)

def print_database_contents(by_id=None, export=False):
    if not os.path.exists(DATABASE_FILE):
        print(f"Database file '{DATABASE_FILE}' does not exist.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        cur.execute('PRAGMA table_info(person)')
        columns = [row['name'] for row in cur.fetchall()]
        if not columns:
            print("No columns found in the 'person' table.", file=sys.stderr)
            sys.exit(1)

        if export:
            cur.execute('SELECT * FROM person')
            rows = cur.fetchall()
            data = {}
            for row in rows:
                data[row['id']] = {key: row[key] for key in row.keys() if key != 'id'}
            with open(EXPORT_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Exported database contents to '{EXPORT_FILE}'")
        elif by_id is not None:
            cur.execute('SELECT * FROM person WHERE id = ?', (by_id,))
            row = cur.fetchone()
            if row is None:
                print(f"No entry with ID {by_id} found.")
                sys.exit(1)
            for key in row.keys():
                if key == 'id':
                    continue
                print(f"{key.capitalize()}={row[key]}")
        else:
            print("Columns in 'person' table:")
            for col in columns:
                print(col)
    except sqlite3.OperationalError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='lsbio – print juror information')
    parser.add_argument('--version', action='version', version='lsbio v0.0')
    parser.add_argument('-i', '--by-id', type=int, help='Show records for specified ID')
    parser.add_argument('-e', '--export', action='store_true', help='Export full database as JSON')
    args = parser.parse_args()

    check_environment_variables()
    print_database_contents(by_id=args.by_id, export=args.export)

if __name__ == '__main__':
    main()