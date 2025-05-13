#!/usr/bin/env python3
import os
import sys
import argparse

# fallback variables
DATABASE_FILE = os.environ.get('DATABASE_FILE', 'juror.db')

def check_environment_variables():
    if 'DATABASE_FILE' not in os.environ:
        print(f"Warning: DATABASE_FILE location is not set. Defaulting to {os.getcwd()}/{DATABASE_FILE}", file=sys.stderr)
    # missing = []
    # for var in ['DATABASE_FILE', 'API_ENDPOINT']:
    #     if var not in os.environ:
    #         print(f"Warning: Environment variable '{var}' is not set.", file=sys.stderr)
    #         missing.append(var)
    # return missing

def main():
    parser = argparse.ArgumentParser(
        description='lsbio – print juror information'
    )
    parser.add_argument('--version', action='version', version='lsbio v0.0')
    args = parser.parse_args()

    check_environment_variables()
    # Your logic here

if __name__ == '__main__':
    main()