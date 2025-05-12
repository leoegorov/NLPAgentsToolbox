# 1. Take a person by ID
# 2. If not exist, create columns FIRST_NAME LAST_NAME
# 3. Ask interactively for first and last name
# 4. Append to table



import pandas as pd
import random

# Load name files
def load_name_file(path):
    df = pd.read_csv(path)
    return df['Name'].tolist(), df['Probability'].tolist()


# Generate a full name based on gender
def generate_full_name(gender):
    if gender == 'Male':
        first_names, first_probs = load_name_file('namesCSV/top_200_male_names.csv')
    elif gender == 'Female':
        first_names, first_probs = load_name_file('namesCSV/top_200_female_names.csv')
    else:
        raise ValueError("Gender must be 'male' or 'female'")

    last_names, last_probs = load_name_file('namesCSV/top_200_last_names.csv')

    first = random.choices(first_names, weights=first_probs, k=1)[0]
    last = random.choices(last_names, weights=last_probs, k=1)[0]
    return f"{first} {last}"

# Interactive prompt
def getFullName(gender):
    full_name = ""
    while True:
        full_name = generate_full_name(gender)
        print(f"\nSuggested name: {full_name}")
        choice = input("Accept (a), New generated suggestion (n), or Enter name of you own (e)? ").strip().lower()
        if choice == 'a':
            print(f"✅ Name accepted: {full_name}")
            return full_name
        elif choice == 'e':
            name = input("Enter full name here: ")
            if len(name.split(' ')) > 1:
                return name
            else:
                print("Please enter a full name!")





def addName(bioWithoutName):
    gender = bioWithoutName[1]
    fullName = getFullName(gender)
    splitName = fullName.split(' ')
    bioWithName = bioWithoutName + [splitName[0], splitName[1]]
    print(bioWithName)
    return bioWithName







