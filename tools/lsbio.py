#!/usr/bin/env python3
import sqlite3
import os
import sys
import argparse
import json
import yaml

# Global variables
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('PROJECT_ROOT', PROJECT_ROOT)
build_dir = os.path.join(PROJECT_ROOT, 'build')
# os.makedirs(build_dir, exist_ok=True)
DATABASE_FILE = os.path.join(build_dir, 'juror.db')
os.environ.setdefault('DATABASE_FILE', DATABASE_FILE)
EXPORT_JSON = os.path.join(build_dir, 'jurors.json')
os.environ.setdefault('EXPORT_JSON', EXPORT_JSON)
EXPORT_YAML = os.path.join(build_dir, 'jurors.yaml')
os.environ.setdefault('EXPORT_YAML', EXPORT_YAML)

def check_environment_variables():
    if 'DATABASE_FILE' not in os.environ:
        print(f"Warning: DATABASE_FILE location is not set. Defaulting to {os.getcwd()}/{DATABASE_FILE}", file=sys.stderr)

def print_database_contents(by_id=None, query=None, latest=False, columns=False, all_entries=False, export_json=False, export_yaml=False):
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

        if export_json:
            cur.execute('SELECT * FROM person')
            rows = cur.fetchall()
            data = {}
            for row in rows:
                data[row['id']] = {key: row[key] for key in row.keys() if key != 'id'}
            with open(EXPORT_JSON, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Exported database contents to '{EXPORT_JSON}'")
        elif export_yaml:
            cur.execute('SELECT * FROM person')
            rows = cur.fetchall()
            data = {}
            for row in rows:
                data[row['id']] = {key: row[key] for key in row.keys() if key != 'id'}
            with open(EXPORT_YAML, 'w') as f:
                yaml.dump(data, f)
            print(f"Exported database contents to '{EXPORT_YAML}'")
        elif query:
            cur.execute(query)
            if query.strip().lower().startswith("select"):
                rows = cur.fetchall()
                for row in rows:
                    print(dict(row))
            else:
                conn.commit()
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
    parser.add_argument('-j', '--export-json', action='store_true', help='Export full database as JSON')
    parser.add_argument('-y', '-e', '--export-yaml', action='store_true', help='Export full database as YAML')
    parser.add_argument('-q', '--query', type=str, help='Run a custom SQL query on the person table')
    args = parser.parse_args()

    check_environment_variables()
    # If no specific mode is chosen, default to latest
    if not (args.by_id or args.query or args.columns or args.all or args.export_json or args.export_yaml):
        args.latest = True

    print_database_contents(
        by_id=args.by_id,
        query=args.query,
        latest=args.latest,
        columns=args.columns,
        all_entries=args.all,
        export_json=args.export_json,
        export_yaml=args.export_yaml
    )

if __name__ == '__main__':
    main()