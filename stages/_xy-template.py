#!/usr/bin/env python3
import os
from stages.utils.dbcontroller import get_val, update_db

# Interactive prompt example
def getInput():
    full_name = ""
    while True:
        full_name = "example"
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
    gender = get_val('gender')
    fullName = getInput()
    splitName = fullName.split(' ')
    update_db('first_name', splitName[0])
    update_db('last_name', splitName[1])
