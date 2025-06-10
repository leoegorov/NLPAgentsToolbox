#!/usr/bin/env python3
import os
import sys
import re
import sqlite3
import importlib.util
import argparse
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stages.utils.dbcontroller import update_db_bio_quote, select_bio_quote


def BioQuoteAction(unknown, num_total):
    bio_quotes= {"AGE": dict(), "INCOME": dict(), "RACE": dict(), "EDUCATION": dict(), "OCCUPATION": dict()}
    pattern = re.compile(r'^-+BIO_QUOTE_(\w+)$')
    i = 0
    while i < len(unknown):
        match = pattern.match(unknown[i])
        if match and i + 1 < len(unknown):
            key = match.group(1)
            key_split= key.split("_")
            if key_split[0] not in bio_quotes.keys():
                raise ValueError(f"{key_split[0]} is unknown bio type!")
            key= " ".join(key_split[1:])
            try:
                value = float(unknown[i + 1])
                bio_quotes[key_split[0]][key] = int(value*num_total+1e-13)
                i += 2
            except ValueError:
                print(f"Expected numeric value after {unknown[i]}")
                i += 1
        else:
            i += 1
    
    bioKeys= list(bio_quotes.keys())
    bio_quotes_elements= dict()
    for key in bioKeys:
        bio_quotes_elements[key]= []
        exclude= []
        remain_num= num_total
        for i in bio_quotes[key].keys():
            exclude.append(i)
            remain_num-= bio_quotes[key][i]
            bio_quotes_elements[key]+= [i for _ in range(bio_quotes[key][i])]
        if remain_num<0:
            raise ValueError(f"Bio type {key} percentage sum over 1!")
        bio_quotes_elements[key]+= ["other(-)"+"(-)".join(bio_quotes[key].keys()) for _ in range(remain_num)]
        bio_quotes[key]["other(-)"+"(-)".join(bio_quotes[key].keys())]= remain_num
        random.shuffle(bio_quotes_elements[key])
    return bio_quotes_elements
#test: python tools\mkbio.py -n 9  -BIO_QUOTE_AGE_50_TO_54_YEARS 0.2 -BIO_QUOTE_AGE_55_TO_59_YEARS 0.5 -BIO_QUOTE_RACE_ASIAN_ALONE 0.3 -BIO_QUOTE_RACE_WHITE_ALONE 0.2

def main():
    # random.seed(2)
    parser = argparse.ArgumentParser(description='mkbio – make some American jurors')
    parser.add_argument('-n', '--num', action='store', type=int, default=1, help='Amount of jurors to generate')
    parser.add_argument('--version', action='version', version='mkbio v0.0')
    parser.add_argument('--print-labels', action='store_true', help='Print available census labels (BIO_QUOTE_{census type}_{census value}) and exit')
    parser.add_argument('-BIO_QUOTE_{census type}_{census value}', '--bio_value', action='store', help='Set percentage of certain bio type. 0 means avoid this census label. Accept multiple parses.')
    args, unknown = parser.parse_known_args()
    bio_quotes_elements= BioQuoteAction(unknown, args.num)
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    # Global variables
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('PROJECT_ROOT', PROJECT_ROOT)
    build_dir = os.path.join(PROJECT_ROOT, 'build')
    # os.makedirs(build_dir, exist_ok=True)
    os.environ.setdefault('BUILD_DIR', build_dir)
    database_file = os.path.join(build_dir, 'juror.db')
    os.environ.setdefault('DATABASE_FILE', database_file)

    if args.print_labels:
        from stages._10_base_info import print_labels
        print_labels()
        return

    stages_dir = os.path.join(os.path.dirname(__file__), '..', 'stages')
    stages_dir = os.path.abspath(stages_dir)
    stage_files = []

    for filename in os.listdir(stages_dir):
        # Match files starting with underscore, two digits, underscore, then rest, ending with .py
        match = re.match(r'_([0-9]{2})_.*\.py$', filename)
        if match:
            stage_files.append((int(match.group(1)), filename))

    DATABASE_FILE = os.environ['DATABASE_FILE']

    for i in range(args.num):

        # update bio quote
        for key in bio_quotes_elements:
            update_db_bio_quote(key, bio_quotes_elements[key][i])

        if args.num > 1:   print(f"\nCreating juror {i + 1} of {args.num}")

        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS juror (id INTEGER PRIMARY KEY AUTOINCREMENT)')
        cur.execute('SELECT MAX(id) FROM juror')
        result = cur.fetchone()
        new_id = (result[0] or 0) + 1
        cur.execute('INSERT INTO juror (id) VALUES (?)', (new_id,))
        conn.commit()
        conn.close()

        total_stages = 99
        for index, filename in sorted(stage_files):
            stage_number = index
            stage_name = os.path.splitext(filename)[0].split('_', 1)[1].replace('_', ' ').title()
            print(f'\nStage {stage_number} of {total_stages}: {stage_name}')
            
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