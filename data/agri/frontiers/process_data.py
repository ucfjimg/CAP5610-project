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

# Removing unnecessary columns
for col in EMPTY_COLUMNS:
    if col in cg_df.columns:
        cg_df = cg_df.drop(columns=col, axis=1)

# Filtering out data that contains a specific metric
yield_df = cg_df[cg_df["Data Item"].str.contains("BU / ACRE")]

# Figuring out the commodity counts
commodity_count = yield_df["Commodity"].value_counts()

# Top two results equal to one another?
if (commodity_count.iloc[0] == commodity_count.iloc[1]):
    commodityOne = commodity_count.index[0]
    commodityTwo = commodity_count.index[1]

# Creating new dataframe
crop_df = yield_df[yield_df["Commodity"].isin([commodityOne, commodityTwo])]

# Writing
crop_df.to_csv(PROCESSED_FILE, index=False)