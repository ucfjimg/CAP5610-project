import sys

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Preprocesses the agricultural data

AGRI_RAW_PATH = "../../data/agri/raw/"
AGRI_PROC_PATH = "../../data/agri/processed/"
COMMON_FILE_NAME = "_1960+2009_Annual+Crop.csv"
SUMMARY_PATH = AGRI_RAW_PATH + "State_Summaries/"

# Needed to clean up data
EMPTY_COLUMNS = ["Week Ending", "State ANSI", "Ag District", "Ag District Code", "County", "County ANSI",
    "Zip Code", "Region", "Watershed_code", "Watershed", "CV (%)"]

if (len(sys.argv) != 2):
    print(f'Usage: python3 {sys.argv[0]} <state>')
    sys.exit(-1)

state = sys.argv[1]

# Constructing file paths
agri_raw_state_path = AGRI_RAW_PATH + state + COMMON_FILE_NAME
agri_processed_state_path = AGRI_PROC_PATH + state + COMMON_FILE_NAME

agri_df = pd.read_csv(agri_raw_state_path)

# Drop the following columns, if they exist
for col in EMPTY_COLUMNS:
    if col in agri_df.columns:
        agri_df = agri_df.drop(columns=col, axis=1)

# This is the final line. Additional things should be above
# to fill in/replace bad values
agri_df.to_csv(agri_processed_state_path, index=False)