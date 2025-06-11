#!/usr/bin/env python3
import random
from stages.utils.dbcontroller import get_val, update_db

def get_prejudice_level():
    """
    Simulates assigning a prejudice level between 0.0 and 1.0
    toward ethnicities/races. The distribution is skewed toward
    lower values to reflect social desirability bias.
    """
    level = random.betavariate(2, 5)  # More likely to produce values closer to 0
    while True:
        full_name = "example"
        print(f"Suggested prejudice level (ethnic/racial): {level:.2f}")
        choice = input("Accept (A), new generated suggestion (n) or enter value of your own (e)? ").strip() or 'A'
        if choice == 'A':
            print(f"Value accepted: {level}")
            return level
        elif choice == 'e':
            level = input("Enter prejudice value: ")
            # todo : check if value in range 0.0 , 1.0
            return level

def main():
    prejudice_level = get_prejudice_level()
    update_db('prejudice', prejudice_level)

if __name__ == "__main__":
    main()