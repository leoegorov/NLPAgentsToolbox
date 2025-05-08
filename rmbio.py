#!/usr/bin/env python3
import os
import sys
import argparse

# fallback variables
DATABASE_FILE = os.environ.get('DATABASE_FILE', 'juror.db')

def check_environment_variables():
    if 'DATABASE_FILE' not in os.environ:
        print(f"Warning: DATABASE_FILE location is not set. Defaulting to {os.getcwd()}/{DATABASE_FILE}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description='rmbio – remove jurors from the database'
    )
    parser.add_argument('--version', action='version', version='rmbio v0.0')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--id', type=int, help='Remove juror by ID')
    group.add_argument('-a', '--all', action='store_true', help='Remove all jurors')

    args = parser.parse_args()
    check_environment_variables()

    import sqlite3
    if not os.path.exists(DATABASE_FILE):
        print(f"Database file '{DATABASE_FILE}' does not exist.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    try:
        if args.id is not None:
            cur.execute('DELETE FROM person WHERE id = ?', (args.id,))
            print(f"Removed juror with ID {args.id}")
        elif args.all:
            cur.execute('DELETE FROM person')
            print("Removed all jurors.")
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()

if __name__ == '__main__':
    main()