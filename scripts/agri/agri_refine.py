import sys

import pandas as pd

AGRI_DATA_PATH = "../../data/agri/"
COMMON_FILE_NAME = "_1960+2009_Annual+Crop+Data.csv"
SUMMARY_PATH = AGRI_DATA_PATH + "State_Summaries/"

if (len(sys.argv) != 2):
    print(f'Usage: python3 {sys.argv[0]} <state>')
    sys.exit(-1)

state = sys.argv[1]

# Constructing file paths
agri_state_path = AGRI_DATA_PATH + state + COMMON_FILE_NAME
state_year_summary = SUMMARY_PATH + state + "_Year_Summary.csv"

# Accessing Year Summary data
year_summary_df = pd.read_csv(state_year_summary)
num_entries = len(year_summary_df.index)

year = year_summary_df.at[num_entries - 1, "Year"]

# Accessing Annual Crop data
agri_df = pd.read_csv(agri_state_path)

agri_year_df = agri_df[agri_df["Year"].isin([year])]

# Collecting all number of unique items that occur
program_list = agri_year_df["Program"].unique()
commodity_list = agri_year_df["Commodity"].unique()
data_item_list = agri_year_df["Data Item"].unique()

# Collecting important data needed for developing the model
summary_final = {}
summary_final["Program"] = program_list
summary_final["Commodity"] = commodity_list
summary_final["Data Item"] = data_item_list

summary_final_path = SUMMARY_PATH + "Final_Summaries/" + state + "_Final+Summary.txt" 

# Writing a final summary of obtained data
with open(summary_final_path, "w") as fp:

    msg = "The following is a summary for the state of %s for the year %d.\n" % (state, year)
    msg += "The selected year has the least number of entries associated with it.\n\n"

    fp.write(msg)

    for k in summary_final.keys():
        k_string = k + "\n\t"
        fp.write(k_string)

        for item in summary_final[k]:
            item_string = item + "\n\t"
            fp.write(item_string)
        
        fp.write('\n')