#!/usr/bin/env python3
import os
from stages.utils.dbcontroller import get_val, update_db

def get_goal():
    print("\nPlease describe the goal for this juror.")
    goal = ""
    while not goal.strip():
        goal = input("Enter the goal: ").strip()
        if not goal:
            print("Goal cannot be empty. Please try again.")
    return goal

def main():
    print("\n")
    goal = get_goal()
    update_db('goal', goal)
