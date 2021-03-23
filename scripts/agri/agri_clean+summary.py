# Removes unneeded columns, keeps the remainder. Summarizes the data in each
# column by number of occurrences for each feature.

import sys

import pandas as pd
import numpy as np

AGRI_DATA_PATH = "../../data/agri/"
COMMON_FILE_NAME = "_1960+2009_Annual+Crop+Data.csv"
SUMMARY_PATH = AGRI_DATA_PATH + "State_Summaries/"

# Needed to clean up data
TRASH_COLUMNS = ["Week Ending", "Geo Level", "Period", "State ANSI", "State", "watershed_code", "Ag District", 
    "Ag District Code", "County", "County ANSI", "Zip Code", "Region", "Watershed", "CV (%)"]

if (len(sys.argv) != 2):
    print(f'Usage: python3 {sys.argv[0]} <state>')
    sys.exit(-1)

state = sys.argv[1]

# Constructing file paths
agri_state_path = AGRI_DATA_PATH + state + COMMON_FILE_NAME

agri_df = pd.read_csv(agri_state_path)
agri_cols = agri_df.columns

# Drop the following columns, if they exist
for col in TRASH_COLUMNS:
    if col in agri_df.columns:
        agri_df = agri_df.drop(columns=col, axis=1)

# Collecting data of all possible values
state_summary = {}

for col in agri_df.columns:
    state_summary[col] = agri_df[col].value_counts()

agri_df.to_csv(agri_state_path, index=False)

for k in state_summary.keys():

    state_summary_path = SUMMARY_PATH + state + "_" + k + "_Summary.csv"

    name = k
    labels = list(state_summary[k].index)
    values = state_summary[k].values

    summary = {}
    summary[name] = labels
    summary["Value Counts"] = values

    summary_df = pd.DataFrame(data=summary)
    summary_df.to_csv(state_summary_path, index=False)
