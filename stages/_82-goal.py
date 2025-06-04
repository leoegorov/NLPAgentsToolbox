#!/usr/bin/env python3
import os
from stages.utils.dbcontroller import get_val, update_db

def get_goal():
    print("\nWould you like to provide a goal for this juror? (y/N)")
    response = input("Your choice: ").strip() or "N"
    if response in ['n', 'no', 'N']:
        return ""
    
    print("Optional: Please describe the goal for this juror.")
    # goal = ""
    # while not goal.strip():
    goal = input("Enter the goal: ").strip()
    if not goal:
        print("No goal set for juror.")
    return goal

def main():
    goal = get_goal()
    if goal:
        update_db('goal', goal)
