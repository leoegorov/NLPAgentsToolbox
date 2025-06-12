#!/usr/bin/env python3
import os
from stages.utils.dbcontroller import get_val, update_db

def get_goal():
    example_goals = [
        "Listen impartially to all sides and help the group reach a fair and just decision.",
        "Don’t sugarcoat your thoughts — say what needs to be said, even if others can’t handle it.",
        "Carefully examine the evidence and call out any nonsense you hear.",
        "Encourage empathy and remind others of the human impact of your verdict.",
        "Stand firm in your principles, even if it means being the lone voice of dissent."
    ]


    print("\nChoose a goal for the juror:")
    print("0. No role")
    print("1. Write your own goal")

    STARTING_INDEX = 2
    for i, goal in enumerate(example_goals, start=STARTING_INDEX):
        print(f"{i}. {goal}")


    while True:
        choice = input("\nEnter the number of the goal you want (or 0 for no role, 1 to write your own): ").strip()
        if choice.isdigit():
            choice = int(choice)
            if STARTING_INDEX <= choice <= len(example_goals) + STARTING_INDEX:
                return example_goals[choice - STARTING_INDEX]
            elif choice == 1:
                custom_goal = input("Write your custom goal: ").strip()
                return custom_goal
            elif choice == 0:
                return ""
        print("Invalid input. Please enter a number between 0 and 5.")

def main():
    goal = get_goal()
    if goal:
        update_db('goal', goal)
