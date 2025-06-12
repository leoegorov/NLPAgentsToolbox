#!/usr/bin/env python3
import os
import pandas as pd # type: ignore
import random
from stages.utils.dbcontroller import get_val, update_db

PROJECT_ROOT  = os.environ['PROJECT_ROOT']

# Load name files
def load_name_file(path):
    df = pd.read_csv(path)
    return df['Name'].tolist(), df['Probability'].tolist()

# Generate a full name based on gender
def generate_full_name(gender):
    if gender == 'Male':
        first_names, first_probs = load_name_file(os.path.join(PROJECT_ROOT, 'stages', 'utils', 'namesCSV', 'top_200_male_names.csv'))
    elif gender == 'Female':
        first_names, first_probs = load_name_file(os.path.join(PROJECT_ROOT, 'stages', 'utils', 'namesCSV', 'top_200_female_names.csv'))
    else:
        raise ValueError("\033[93mGender must be 'male' or 'female'\033[0m")

    last_names, last_probs = load_name_file(os.path.join(PROJECT_ROOT, 'stages', 'utils', 'namesCSV', 'top_200_last_names.csv'))

    first = random.choices(first_names, weights=first_probs, k=1)[0]
    last = random.choices(last_names, weights=last_probs, k=1)[0]
    return f"{first} {last}"

# Interactive prompt
def getFullName(gender):
    full_name = ""
    while True:
        full_name = generate_full_name(gender)
        print(f"Suggested name: {full_name}")
        #choice = input("Accept (A), new generated suggestion (n) or enter name of your own (e)? ").strip() or 'A'
        choice = 'A'
        if choice == 'A':
            print(f"Name accepted: {full_name}")
            return full_name
        elif choice == 'e':
            name = input("Enter full name here: ")
            if len(name.split(' ')) > 1:
                return name
            else:
                print("Please enter a full name!")

def main():
    gender = get_val('gender')
    fullName = getFullName(gender)
    split_name = fullName.split(' ')
    first_name = split_name[0]
    last_name = split_name[-1]
    middle_name = ' '.join(split_name[1:-1]) if len(split_name) > 2 else ''

    update_db('first_name', first_name)
    update_db('last_name', last_name)
    if middle_name:
        update_db('middle_name', middle_name)
