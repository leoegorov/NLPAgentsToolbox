#!/usr/bin/env python3
import os
from stages.utils.dbcontroller import get_val, update_db

def get_role():
    print("Please describe the role for this juror.")
    role = ""
    while not role.strip():
        #role = input("Enter the role: ").strip()
        role = "You are a juror in a case"
        if not role:
            print("Role cannot be empty. Please try again.")
    return role

def main():
    role = get_role()
    update_db('role', role)
