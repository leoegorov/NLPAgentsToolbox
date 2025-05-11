#!/usr/bin/env python3
import requests # type: ignore
import random
import sqlite3
import os
import sys
import argparse

# fallback variables
DATABASE_FILE = os.environ.get('DATABASE_FILE', 'juror.db')
API_CENSUS  = os.environ.get('API_CENSUS', 'https://api.census.gov/data/2020/dec/pl')
# API_KEY = None  # Optional: Replace with your key like 'your_api_key_here'

def check_environment_variables():
    if 'DATABASE_FILE' not in os.environ:
        print(f"Warning: DATABASE_FILE location is not set. Defaulting to {os.getcwd()}/{DATABASE_FILE}", file=sys.stderr)

# Get list of U.S. states and populations
def fetch_state_populations():
    params = {
        'get': 'NAME,P1_001N',
        'for': 'state:*'
    }
    # if API_KEY:
    #     params['key'] = API_KEY

    response = requests.get(API_CENSUS, params=params)
    data = response.json()
    headers, rows = data[0], data[1:]
    return [(row[0], int(row[1]), row[2]) for row in rows]  # (state_name, population, state_code)

# Select a random state based on population
def select_state_weighted(states):
    names = [s[0] for s in states]
    weights = [s[1] for s in states]
    chosen_index = random.choices(range(len(states)), weights=weights)[0]
    return states[chosen_index]

# Generate random age and gender
def generate_random_person():
    gender = random.choice(['Male', 'Female'])
    return gender

# Get list of U.S. popolation vs age
def fetch_pop_age(gender= "m"):
    ageDivision= [f"B01001_{i+3:03d}E" for i in range(8, 23)]
    if gender== "f":
        ageDivision= [f"B01001_{i+3:03d}E" for i in range(8, 23)]
    params = {
            'get': ",".join(ageDivision),
            'for': 'us:*'
        }
    tmpAPI= "https://api.census.gov/data/2023/acs/acs1"
    variableURL= tmpAPI+"/variables.json"
    response = requests.get(variableURL)
    variable = response.json()
    response = requests.get(tmpAPI, params= params)
    agePopData = response.json()
    label= [variable["variables"][i]["label"].split("!!")[-1] for i in agePopData[0][0: -1]]
    # print(label)
    pop= [int(i) for i in agePopData[1][0: -1]]
    agePopWeight= [label, pop]
    return agePopWeight

# Get list of U.S. family vs annual income
def fetch_family_income():
    division= [f"B19101A_{i+2:03d}E" for i in range(16)]
    # print(division)
    params = {
            'get': ",".join(division),
            'for': 'us:*'
        }
    tmpAPI= "https://api.census.gov/data/2023/acs/acs1"
    variableURL= tmpAPI+"/variables.json"
    response = requests.get(variableURL)
    variable = response.json()
    response = requests.get(tmpAPI, params= params)
    tmpData = response.json()
    label= [variable["variables"][i]["label"].split("!!")[-1] for i in tmpData[0][0: -1]]
    pop= [int(i) for i in tmpData[1][0: -1]]
    namePopWeight= [label, pop]
    return namePopWeight

# Get list of U.S. population vs one race, whole age
def fetch_pop_singleRace(state= 1):
    division= ["P11_008N", "P9_007N", "P9_009N", "P9_005N", "P9_006N"]
    # print(division)
    params = {
            'get': ",".join(division),
            'for': f'state:{state:02d}'
        }
    tmpAPI= "https://api.census.gov/data/2020/dec/cd118"
    variableURL= tmpAPI+"/variables.json"
    response = requests.get(variableURL)
    variable = response.json()
    label= [variable["variables"][i]["label"].split("!!")[-1] for i in division]
    response = requests.get(tmpAPI, params= params)
    tmpData = response.json()
    pop= [int(i) for i in tmpData[1][0: -1]]
    namePopWeight= [label, pop]
    return namePopWeight

# Get list of U.S. population vs one education level, 25 and over
def fetch_pop_education(gender= "f", state= 1):
    division= [f"S1501_C05_{i+7:03d}E" for i in range(7)]
    if gender== "f":
        division= [f"S1501_C03_{i+7:03d}E" for i in range(7)]
    # print(division)
    params = {
            'get': ",".join(division),
            'for': f'state:{state:02d}'
        }
    tmpAPI= "https://api.census.gov/data/2023/acs/acs1/subject"
    variableURL= tmpAPI+"/variables.json"
    response = requests.get(variableURL)
    variable = response.json()
    label= [variable["variables"][i]["label"].split("!!")[-1] for i in division]
    # print(label)
    response = requests.get(tmpAPI, params= params)
    tmpData = response.json()
    pop= [int(i) for i in tmpData[1][0: -1]]
    namePopWeight= [label, pop]
    return namePopWeight

def fetch_pop_occupation(gender= "f"):
    division= [f"S2401_C02_{i+2:03d}E" for i in range(35)]
    if gender== "f":
        division= [f"S2401_C04_{i+2:03d}E" for i in range(35)]
    params = {
            'get': ",".join(division),
            'for': f'us:*'
        }
    tmpAPI= "https://api.census.gov/data/2023/acs/acs1/subject"
    variableURL= tmpAPI+"/variables.json"
    response = requests.get(variableURL)
    variable = response.json()
    label= [variable["variables"][i]["label"].split("!!")[-1] for i in division]
    response = requests.get(tmpAPI, params= params)
    tmpData = response.json()
    pop= [int(i) for i in tmpData[1][0: -1]]
    namePopWeight= [label, pop]
    return namePopWeight

def select_name_weighted(nameWeight):
    names = nameWeight[0]
    weights = nameWeight[1]
    chosen_index = random.choices(range(len(names)), weights=weights)[0]
    return names[chosen_index]

# Initialize and write to SQLite
def save_person_to_db(traits):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    #[gender, age, state_name, income, race, edu, occupation]
    cur.execute('''
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            gender TEXT,
            state TEXT,
            income TEXT,
            race TEXT,
            edu TEXT,
            occupation TEXT
        )
    ''')
    cur.execute('INSERT INTO person (age, gender, state, income, race, edu, occupation) VALUES (?, ?, ?, ?, ?, ?, ?)', traits)
    conn.commit()
    conn.close()

def main():
    parser = argparse.ArgumentParser(
        description='mkbio – create an American and call make them a juror'
    )
    parser.add_argument('--version', action='version', version='mkbio v0.0')
    args = parser.parse_args()

    check_environment_variables()
    print("Fetching U.S. population data by state...")
    states = fetch_state_populations()
    print("Fetching U.S. population data by state...")
    state_name, _, stateID = select_state_weighted(states)
    gender = generate_random_person()
    print("Fetching U.S. age data by gender...")
    agePopWeight= fetch_pop_age(gender)
    age= select_name_weighted(agePopWeight)
    print("Fetching U.S. income data...")
    incomePopWeight= fetch_family_income()
    income= select_name_weighted(incomePopWeight)
    print("Fetching U.S. race data by state...")
    racePopWeight= fetch_pop_singleRace(int(stateID))
    race= select_name_weighted(racePopWeight)
    print("Fetching U.S. education data by state and gender...")
    eduPopWeight= fetch_pop_education(gender, int(stateID))
    edu= select_name_weighted(eduPopWeight)
    print("Fetching U.S. occupation data by gender...")
    occupationPopWeight= fetch_pop_occupation(gender)
    occupation= select_name_weighted(occupationPopWeight)
    traits= [age, gender, state_name, income, race, edu, occupation]
    print(traits)
    save_person_to_db(traits)

    # print(f"Installed as juror: Age={age}, Gender={gender}, State={state_name}")

if __name__ == '__main__':
    main()