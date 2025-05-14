#!/usr/bin/env python3
import os
import pandas as pd # type: ignore
import random
from stages.utils.dbcontroller import get_val, update_db

DATABASE_FILE = os.environ['DATABASE_FILE']


# Load name files
def load_name_file(path):
    df = pd.read_csv(path)
    return df['Name'].tolist(), df['Probability'].tolist()

# Generate a full name based on gender
def generate_full_name(gender):
    if gender == 'Male':
        first_names, first_probs = load_name_file('stages/utils/namesCSV/top_200_male_names.csv')
    elif gender == 'Female':
        first_names, first_probs = load_name_file('stages/utils/namesCSV/top_200_female_names.csv')
    else:
        raise ValueError("Gender must be 'male' or 'female'")

    last_names, last_probs = load_name_file('stages/utils/namesCSV/top_200_last_names.csv')

    first = random.choices(first_names, weights=first_probs, k=1)[0]
    last = random.choices(last_names, weights=last_probs, k=1)[0]
    return f"{first} {last}"

# Interactive prompt
def getFullName(gender):
    full_name = ""
    while True:
        full_name = generate_full_name(gender)
        print(f"Suggested name: {full_name}")
        choice = input("Accept (A), new generated suggestion (n) or enter name of your own (e)? ").strip() or 'A'
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
    print("\n")
    gender = get_val('GENDER')
    fullName = getFullName(gender)
    splitName = fullName.split(' ')
    update_db('FIRST_NAME', splitName[0])
    update_db('LAST_NAME', splitName[1])
