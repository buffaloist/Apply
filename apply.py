#!/usr/bin/env python3
# don't take this too seriously, job hunting sucks

import sys
from argparse import ArgumentParser as aparse
import os
import pandas
from datetime import datetime, timedelta

# remember to change this path and file name
database = '/Path/to/applications.csv'

def create_parser():
    parser = aparse(description="""
    applications.py: return statistics about your job applications.
    """)

    parser.add_argument('todo', choices=['basic', 'compare', 'hope', 'nohope'], help='basic: Print basic stats, compare: show number of open versus rejected applications, hope: get some hope, nohope: lose all hope')
    
    return parser

def main():
    # check if file exists, create if it does not
    if not os.path.exists(database):
        with open(database, "w") as file:
            headings = 'company name,position,application date,response date,response,notes'
            file.write(headings)
    
    fix_case()
    args = create_parser().parse_args()
    
    if args.todo == 'basic':
        basic()
    elif args.todo == 'compare':
        compare()
    elif args.todo == 'hope':
        hope()
    elif args.todo == 'nohope':
        nohope()
    else:
        print("Please refer to help and use a valid argument.")
        sys.exit(0)

def basic():
    print("\n")
    f = open(database, "r")
    a = 0
    y = 0
    n = 0
    for x in f:
        if "negative" in x:
            n += 1
        if "positive" in x:
            y += 1
        a += 1
    print(f"You have filled out {a} applications, have been turned down {n} times, have {y} positive responses, and {a - (y + n)} companies have not responded to you.")
    print("\n")
    f.close()

def compare():
    print("\n")
    df = pandas.read_csv(database)
    df['application date'] = pandas.to_datetime(df['application date'], format="%Y-%m-%d")
    df['response date'] = pandas.to_datetime(df['response date'], format="%Y-%m-%d")
    open_apps = df[df['response'].isnull()].shape[0]
    rejects = df[df['response'] == 'negative'].shape[0]
    positives = df[df['response'] == 'positive'].shape[0]
    print(f"There are {open_apps} open applications, {rejects} rejected applications, and {positives} applications with positive responses.")    
    print("\n")

def hope():
    print("\n")
    df = pandas.read_csv(database)
    df['application date'] = pandas.to_datetime(df['application date'], format="%Y-%m-%d")
    df['response date'] = pandas.to_datetime(df['response date'], format="%Y-%m-%d")
    filtered = df[df['response'] == 'positive' ]
    filtered = filtered[['company name', 'position', 'response date', 'notes']]
    print(filtered)
    print("\n")
    
    last_month = datetime.now() - timedelta(days=30)
    new_applications = df[(df['response'].isnull()) & (df['application date'] > last_month)].shape[0]
    # TODO print number of applications awaiting on response less than a month old
    print(f"There are {new_applications} applications awaiting response that are less than a month old.")
    print("\n")

def nohope():
    df = pandas.read_csv(database)
    df['application date'] = pandas.to_datetime(df['application date'], format="%Y-%m-%d")
    df['response date'] = pandas.to_datetime(df['response date'], format="%Y-%m-%d")
    print("\n")
    two_months = datetime.now() - timedelta(days=60)
    turned_down = df[df['response'] == 'negative'].shape[0]
    stale_apps = df[(df['response'].isnull()) & (df['application date'] < two_months)].shape[0]
    print(f"You have been turned down {turned_down} times and have {stale_apps} applications that are so old they should be considered lost.")
    print("\n")

def fix_case():
    with open(database, 'r') as file:
        content = file.read()
    lowercase_content = content.lower()
    with open(database, 'w') as file:
        file.write(lowercase_content)

if __name__ == "__main__":
    main()
