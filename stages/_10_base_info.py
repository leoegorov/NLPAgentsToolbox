#!/usr/bin/env python3
from datetime import timedelta
import random
import sqlite3
import os
import sys
import argparse
import requests_cache # type: ignore
from stages.utils.dbcontroller import update_db, select_bio_quote
from collections import defaultdict
import re

os.environ.setdefault('API_CENSUS', 'https://api.census.gov/data/2020/dec/pl')
API_CENSUS = os.environ['API_CENSUS']
BUILD_DIR  = os.environ['BUILD_DIR']

list_only = False

def normalize_label(label):
    return re.sub(r'[^a-z0-9]+', '_', label.lower()).strip('_')

def parse_user_quote_env(prefix, labels, pops):
    normalized_labels = [normalize_label(label) for label in labels]
    quote_env = {label: float(os.environ.get(f"{prefix}_{label.upper()}", -1)) for label in normalized_labels}
    user_defined = {k: v for k, v in quote_env.items() if v >= 0}
    if sum(user_defined.values()) > 1.0:
        raise ValueError(f"{prefix} quote sum exceeds 100%: {sum(user_defined.values())}")
    remaining = 1.0 - sum(user_defined.values())
    remaining_labels = [lbl for lbl, norm in zip(labels, normalized_labels) if quote_env[norm] == -1]
    remaining_pops = [pops[labels.index(lbl)] for lbl in remaining_labels]
    remaining_total = sum(remaining_pops)
    adjusted = {normalize_label(lbl): pop / remaining_total * remaining for lbl, pop in zip(remaining_labels, remaining_pops)}
    full_dist = {**user_defined, **adjusted}
    return labels, [full_dist[normalize_label(label)] for label in labels]

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
    label, pop = label, pop
    labels, weights = parse_user_quote_env("BIO_QUOTE_AGE", label, pop)
    return [labels, weights]

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
    labels, weights = parse_user_quote_env("BIO_QUOTE_INCOME", label, pop)
    return [labels, weights]

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
    label, pop = label, pop
    labels, weights = parse_user_quote_env("BIO_QUOTE_RACE", label, pop)
    return [labels, weights]

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
    labels, weights = parse_user_quote_env("BIO_QUOTE_EDUCATION", label, pop)
    return [labels, weights]

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
    columns = data[0]
    filtered_cols = [
        col for col in columns 
        if col != 'NAME' and col.endswith('E') 
        and not col.endswith('EA') and not col.endswith('M') and not col.endswith('MA')
    ]
    nameID = filtered_cols
    nameAmount = [int(data[1][columns.index(col)]) for col in filtered_cols]
    label= [variable["variables"][i[:-1]+"E"]["label"].split("!!")[-1] for i in nameID]
    labels, weights = parse_user_quote_env("BIO_QUOTE_OCCUPATION", label, nameAmount)
    return [labels, weights]

def select_name_weighted(nameWeight):
    names = nameWeight[0]
    weights = nameWeight[1]
    chosen_index = random.choices(range(len(names)), weights=weights)[0]
    return names[chosen_index]

def print_labels():
    global list_only 
    list_only = True
    main()

def rebuild_quote_pop_weight(key, PopWeight):
    tmp_quote= select_bio_quote(key)
    if tmp_quote== None:
        return PopWeight
    labels= [i.upper() for i in PopWeight[0]]
    splitTmp= tmp_quote.split("(-)")
    if len(splitTmp)>1:
        for item in splitTmp[1:]:
            if len(item):
                try:
                    index_tmp = labels.index(item)
                    PopWeight[1][index_tmp]= 0
                except ValueError:
                    raise ValueError(f"Bio type {key}, {item} is incorrect input!")
    else:
        if tmp_quote not in labels:
            raise ValueError(f"Bio type {key}, {tmp_quote} is incorrect input!")
        orin_index= labels.index(tmp_quote)
        PopWeight= [[PopWeight[0][orin_index]], [1]] 
    return PopWeight

def main():
    # cache visited website for better performance
    cache_path = os.path.join(BUILD_DIR, 'request_cache')
    session = requests_cache.CachedSession(cache_path, expire_after=timedelta(hours=2))

    # print("Fetching U.S. population data by state...")
    states = fetch_state_populations(session)
    # print("Fetching U.S. population data by state...")
    state_name, _, stateID = select_state_weighted(states)
    gender = generate_random_person()
    # print("Fetching U.S. age data by gender...")
    agePopWeight= fetch_pop_age(gender, session)
    agePopWeight= rebuild_quote_pop_weight("AGE", agePopWeight)
    age= select_name_weighted(agePopWeight)
    # print("Fetching U.S. income data...")
    incomePopWeight= fetch_family_income(session)
    incomePopWeight= rebuild_quote_pop_weight("INCOME", incomePopWeight)
    income= select_name_weighted(incomePopWeight)
    # print("Fetching U.S. race data by state...")
    racePopWeight= fetch_pop_singleRace(int(stateID), session)
    racePopWeight= rebuild_quote_pop_weight("RACE", racePopWeight)
    race= select_name_weighted(racePopWeight)
    # print("Fetching U.S. education data by state and gender...")
    eduPopWeight= fetch_pop_education(gender, int(stateID), session)
    eduPopWeight= rebuild_quote_pop_weight("EDUCATION", eduPopWeight)
    edu= select_name_weighted(eduPopWeight)
    # print("Fetching U.S. occupation data by gender...")
    occupationPopWeight= fetch_pop_occupation(gender, session)
    occupationPopWeight= rebuild_quote_pop_weight("OCCUPATION", occupationPopWeight)
    occupation= select_name_weighted(occupationPopWeight)

    # print labels and exit if called with --print-income-labels 
    if list_only:
        for label in agePopWeight[0]:
            print(f"BIO_QUOTE_AGE_{normalize_label(label.upper())}")
        for label in incomePopWeight[0]:
            print(f"BIO_QUOTE_INCOME_{normalize_label(label.upper())}")
        for label in racePopWeight[0]:
            print(f"BIO_QUOTE_RACE_{normalize_label(label.upper())}")
        for label in eduPopWeight[0]:
            print(f"BIO_QUOTE_EDUCATION_{normalize_label(label.upper())}")
        for label in occupationPopWeight[0]:
            print(f"BIO_QUOTE_OCCUPATION_{normalize_label(label.upper())}")
        exit(0)

    # update database
    update_db("age", age)
    update_db("gender", gender)
    update_db("state", state_name)
    update_db("income", income)
    update_db("race", race)
    update_db("education", edu)
    update_db("occupation", occupation)
    
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
