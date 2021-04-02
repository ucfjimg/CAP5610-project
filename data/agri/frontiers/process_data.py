import sys

import pandas as pd
import numpy as np

# Preprocesses the Cerro Gordo County, Iowa crop data

FILE_NAME = "Iowa+Cerro+Gordo_1960+2009_Annual+Crop.csv"
PROCESSED_FILE = "Processed_Iowa+Cerro+Gordo_1960+2009_Annual+Crop.csv"

EMPTY_COLUMNS = ["Week Ending", "State ANSI", "Ag District Code", "County ANSI", "Zip Code",
    "Region", "watershed_code", "Watershed", "Domain", "CV (%)"]

# Open the data
cg_df = pd.read_csv(FILE_NAME)

for col in EMPTY_COLUMNS:
    if col in cg_df.columns:
        cg_df = cg_df.drop(columns=col, axis=1)

cg_df.to_csv(PROCESSED_FILE, index=False)