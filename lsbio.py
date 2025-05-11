#!/usr/bin/env python3
import sqlite3
import os
import sys
import argparse

# fallback variables
DATABASE_FILE = os.environ.get('DATABASE_FILE', 'juror.db')

def format_list(dataList):
    lenRestrict= [3, 15, 7, 15, 20, 20, 20, 20]
    dataList= [f"{dataList[i]:<{lenRestrict[i]}}" for i in range(len(dataList))]
    return dataList

def check_environment_variables():
    if 'DATABASE_FILE' not in os.environ:
        print(f"Warning: DATABASE_FILE location is not set. Defaulting to {os.getcwd()}/{DATABASE_FILE}", file=sys.stderr)

def print_database_contents():
    if not os.path.exists(DATABASE_FILE):
        print(f"Database file '{DATABASE_FILE}' does not exist.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    try:
        cur.execute('SELECT * FROM person')
        rows = cur.fetchall()
        header= format_list([i[0] for i in cur.description])
        if not rows:
            print("No entries found in the 'person' table.", file=sys.stderr)
            sys.exit(1)

        # print(f"{'ID':<5} {'Age':<5} {'Gender':<8} {'State'}")
        print("".join(header))
        print("-" * 90)
        for row in rows:
            print("".join(format_list(row)))
            # print(f"{row[0]:<5} {row[1]:<5} {row[2]:<8} {row[3]}")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description='lsbio – print juror information'
    )
    parser.add_argument('--version', action='version', version='lsbio v0.0')
    args = parser.parse_args()

    check_environment_variables()
    print_database_contents()

if __name__ == '__main__':
    main()