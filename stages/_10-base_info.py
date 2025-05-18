#!/usr/bin/env python3
from datetime import timedelta
import random
import sqlite3
import os
import sys
import argparse
import requests_cache # type: ignore
from stages.utils.dbcontroller import update_db

API_CENSUS = os.environ['API_CENSUS']

# Get list of U.S. states and populations
def fetch_state_populations(session= None):
    params = {
        'get': 'NAME,P1_001N',
        'for': 'state:*'
    }

    response = session.get(API_CENSUS, params=params)
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
def fetch_pop_age(gender= "m", session= None):
    ageDivision= [f"B01001_{i+3:03d}E" for i in range(8, 23)]
    if gender== "f":
        ageDivision= [f"B01001_{i+3:03d}E" for i in range(8, 23)]
    params = {
            'get': ",".join(ageDivision),
            'for': 'us:*'
        }
    tmpAPI= "https://api.census.gov/data/2023/acs/acs1"
    variableURL= tmpAPI+"/variables.json"
    response = session.get(variableURL)
    variable = response.json()
    response = session.get(tmpAPI, params= params)
    agePopData = response.json()
    label= [variable["variables"][i]["label"].split("!!")[-1] for i in agePopData[0][0: -1]]
    pop= [int(i) for i in agePopData[1][0: -1]]
    agePopWeight= [label, pop]
    return agePopWeight

# Get list of U.S. family vs annual income
def fetch_family_income(session= None):
    division= [f"B19101A_{i+2:03d}E" for i in range(16)]
    params = {
            'get': ",".join(division),
            'for': 'us:*'
        }
    tmpAPI= "https://api.census.gov/data/2023/acs/acs1"
    variableURL= tmpAPI+"/variables.json"
    response = session.get(variableURL)
    variable = response.json()
    response = session.get(tmpAPI, params= params)
    tmpData = response.json()
    label= [variable["variables"][i]["label"].split("!!")[-1] for i in tmpData[0][0: -1]]
    pop= [int(i) for i in tmpData[1][0: -1]]
    namePopWeight= [label, pop]
    return namePopWeight

# Get list of U.S. population vs one race, whole age
def fetch_pop_singleRace(state= 1, session= None):
    division= ["P11_008N", "P9_007N", "P9_009N", "P9_005N", "P9_006N"]
    # print(division)
    params = {
            'get': ",".join(division),
            'for': f'state:{state:02d}'
        }
    tmpAPI= "https://api.census.gov/data/2020/dec/cd118"
    variableURL= tmpAPI+"/variables.json"
    response = session.get(variableURL)
    variable = response.json()
    label= [variable["variables"][i]["label"].split("!!")[-1] for i in division]
    response = session.get(tmpAPI, params= params)
    tmpData = response.json()
    pop= [int(i) for i in tmpData[1][0: -1]]
    namePopWeight= [label, pop]
    return namePopWeight

# Get list of U.S. population vs one education level, 25 and over
def fetch_pop_education(gender= "f", state= 1, session= None):
    division= [f"S1501_C05_{i+7:03d}E" for i in range(7)]
    if gender== "f":
        division= [f"S1501_C03_{i+7:03d}E" for i in range(7)]
    params = {
            'get': ",".join(division),
            'for': f'state:{state:02d}'
        }
    tmpAPI= "https://api.census.gov/data/2023/acs/acs1/subject"
    variableURL= tmpAPI+"/variables.json"
    response = session.get(variableURL)
    variable = response.json()
    label= [variable["variables"][i]["label"].split("!!")[-1] for i in division]
    response = session.get(tmpAPI, params= params)
    tmpData = response.json()
    pop= [int(i) for i in tmpData[1][0: -1]]
    namePopWeight= [label, pop]
    return namePopWeight

def fetch_pop_occupation(gender= "f", session= None):
    toGet= "group(B24125)"
    if gender== "Female":
        toGet= "group(B24126)"
    params = {
            'get': toGet,
            'for': 'us:*'}
    tmpAPI= "https://api.census.gov/data/2023/acs/acs1"
    response = session.get(tmpAPI, params= params)
    data = response.json()
    variableURL= tmpAPI+"/variables.json"
    response = session.get(variableURL)
    variable = response.json()
    lenOfData= len(data[0])//2-3
    nameID= [data[0][i*2+4] for i in range(lenOfData)]
    nameAmount=  [int(data[1][i*2+4]) for i in range(lenOfData)]
    label= [variable["variables"][i[:-1]+"E"]["label"].split("!!")[-1] for i in nameID]
    namePopWeight= [label, nameAmount]
    return namePopWeight

def select_name_weighted(nameWeight):
    names = nameWeight[0]
    weights = nameWeight[1]
    chosen_index = random.choices(range(len(names)), weights=weights)[0]
    return names[chosen_index]

def main():
    # parser = argparse.ArgumentParser(
    #     description='mkbio – create an American and call make them a juror'
    # )
    # parser.add_argument('--version', action='version', version='mkbio v0.0')
    # args = parser.parse_args()

    # cache visited website for better performance
    session = requests_cache.CachedSession('request_cache', expire_after=timedelta(hours=2))

    print("\n")

    print("Fetching U.S. population data by state...")
    states = fetch_state_populations(session)
    print("Fetching U.S. population data by state...")
    state_name, _, stateID = select_state_weighted(states)
    gender = generate_random_person()
    print("Fetching U.S. age data by gender...")
    agePopWeight= fetch_pop_age(gender, session)
    age= select_name_weighted(agePopWeight)
    print("Fetching U.S. income data...")
    incomePopWeight= fetch_family_income(session)
    income= select_name_weighted(incomePopWeight)
    print("Fetching U.S. race data by state...")
    racePopWeight= fetch_pop_singleRace(int(stateID), session)
    race= select_name_weighted(racePopWeight)
    print("Fetching U.S. education data by state and gender...")
    eduPopWeight= fetch_pop_education(gender, int(stateID), session)
    edu= select_name_weighted(eduPopWeight)
    print("Fetching U.S. occupation data by gender...")
    occupationPopWeight= fetch_pop_occupation(gender, session)
    occupation= select_name_weighted(occupationPopWeight)

    # update database
    update_db("AGE", age)
    update_db("GENDER", gender)
    update_db("STATE", state_name)
    update_db("INCOME", income)
    update_db("RACE", race)
    update_db("EDUCATION", edu)
    update_db("OCCUPATION", occupation)
    
    print(f"""Juror base info:
        Age={age}
        Gender={gender}
        State={state_name}
        Income={income}
        Race={race}
        Education={edu}
        Occupation={occupation}""")

if __name__ == '__main__':
    main()
