#!/usr/bin/env python3
import os
from stages.utils.dbcontroller import get_val, update_db

DATABASE_FILE = os.environ['DATABASE_FILE']

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
    gender = get_val('GENDER')
    fullName = getInput()
    splitName = fullName.split(' ')
    update_db('FIRST_NAME', splitName[0])
    update_db('LAST_NAME', splitName[1])
