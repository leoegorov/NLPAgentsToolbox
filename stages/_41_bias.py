#!/usr/bin/env python3
import random
from stages.utils.dbcontroller import get_val, update_db

def collect_biases():
    """
    Collects multiple bias entries from the user in the form bias_against_<race>: value.
    """
    biases = {}
    while True:
        race = input("Enter race/ethnicity (no spaces, or leave empty to finish): ").strip()
        if not race:
            break
        if ' ' in race:
            print("Race/ethnicity must not contain spaces. Please try again.")
            continue
        key = f"bias_against_{race}"
        while True:
            value = input(f"Enter bias value for {race} (0.0 - 1.0): ").strip()
            try:
                value_f = float(value)
                if 0.0 <= value_f <= 1.0:
                    biases[key] = value_f  # Store as float only
                    break
                else:
                    print("Value must be between 0.0 and 1.0.")
            except ValueError:
                print("Please enter a valid number.")
    return biases

def main():
    biases = collect_biases()
    if biases:
        for key, value in biases.items():
            update_db(key, float(value))  # Ensure float is passed
    else:
        print("No biases entered.")

if __name__ == "__main__":
    main()