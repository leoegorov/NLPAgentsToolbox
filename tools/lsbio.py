#!/usr/bin/env python3
import sqlite3
import os
import sys
import argparse
import json

# Global variables
build_dir = os.environ.get('BUILD_DIR', 'build')
# os.makedirs(build_dir, exist_ok=True)
DATABASE_FILE = os.path.join(build_dir, 'juror.db')
os.environ.setdefault('DATABASE_FILE', DATABASE_FILE)
EXPORT_FILE = os.path.join(build_dir, 'export.json')
os.environ.setdefault('EXPORT_FILE', EXPORT_FILE)

def check_environment_variables():
    if 'DATABASE_FILE' not in os.environ:
        print(f"Warning: DATABASE_FILE location is not set. Defaulting to {os.getcwd()}/{DATABASE_FILE}", file=sys.stderr)

def print_database_contents(by_id=None, export=False, query=None, latest=False, columns=False, all_entries=False):
    if not os.path.exists(DATABASE_FILE):
        print(f"Database file '{DATABASE_FILE}' does not exist.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        cur.execute('PRAGMA table_info(person)')
        colnames = [row['name'] for row in cur.fetchall()]
        if not colnames:
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
        elif query:
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                print(dict(row))
            return
        elif by_id is not None:
            cur.execute('SELECT * FROM person WHERE id = ?', (by_id,))
            row = cur.fetchone()
            if row is None:
                print(f"No entry with ID {by_id} found.")
                sys.exit(1)
            for key in row.keys():
                if key == 'Id':
                    continue
                print(f"{key.capitalize()}={row[key]}")
        elif all_entries:
            cur.execute('SELECT id FROM person ORDER BY id')
            ids = [row['id'] for row in cur.fetchall()]
            for pid in ids:
                cur.execute('SELECT * FROM person WHERE id = ?', (pid,))
                row = cur.fetchone()
                print(f"\nId={row['id']}")
                for key in row.keys():
                    if key == 'id':
                        continue
                    print(f"{key.capitalize()}={row[key]}")
        elif columns:
            print("Columns in 'person' table:")
            for col in colnames:
                print(col)
        elif latest:
            cur.execute('SELECT * FROM person ORDER BY id DESC LIMIT 1')
            row = cur.fetchone()
            if row is None:
                print("No entries found in the 'person' table.", file=sys.stderr)
                sys.exit(1)
            for key in row.keys():
                if key == 'Id':
                    continue
                print(f"{key.capitalize()}={row[key]}")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='lsbio – print juror information')
    parser.add_argument('--version', action='version', version='lsbio v0.0')
    parser.add_argument('-c', '--columns', action='store_true', help='List column names only')
    parser.add_argument('-i', '--by-id', type=int, help='Show records for specified ID')
    parser.add_argument('-l', '--latest', action='store_true', help='Show the latest juror entry (default)')
    parser.add_argument('-a', '--all', action='store_true', help='Show all entries')
    parser.add_argument('-e', '--export', action='store_true', help='Export full database as JSON')
    parser.add_argument('-q', '--query', type=str, help='Run a custom SQL query on the person table')
    args = parser.parse_args()

    check_environment_variables()
    # If no specific mode is chosen, default to latest
    if not (args.by_id or args.export or args.query or args.columns or args.all):
        args.latest = True

    print_database_contents(
        by_id=args.by_id,
        export=args.export,
        query=args.query,
        latest=args.latest,
        columns=args.columns,
        all_entries=args.all
    )

if __name__ == '__main__':
    main()