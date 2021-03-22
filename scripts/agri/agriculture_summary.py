# Collates key data (i.e. features and possible vlaues) for further
# processing

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

# Constructing full paths
agri_state_path = AGRI_DATA_PATH + state + COMMON_FILE_NAME
# state_summary_path = SUMMARY_PATH + state + "_Summary.csv"

agri_df = pd.read_csv(agri_state_path)
agri_cols = agri_df.columns

# Drop the following columns, if they exist
for col in TRASH_COLUMNS:
    if col in agri_df.columns:
        agri_df = agri_df.drop(columns=col, axis=1)

# Collecting data of all possible values
state_summary = {}
# state_summary["Commodity"] = agri_df["Commodity"].value_counts()

# print(state_summary)

for col in agri_df.columns:
    state_summary[col] = agri_df[col].value_counts()


# print(state_summary["Commodity"].index)
# print()
# print(state_summary["Commodity"].name)

# summary_df = pd.DataFrame.from_dict(state_summary)

agri_df.to_csv(agri_state_path, index=False)

for k in state_summary.keys():

    state_summary_path = SUMMARY_PATH + state + "_" + k + "_Summary.csv"

    state_summary[k].to_csv(state_summary_path, header=False, index_label=k.index)
