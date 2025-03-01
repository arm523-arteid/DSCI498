"""
Reading the data from GoogleDrive
"""

#import necessary packages
import pandas as pd
import requests
import io

def load_csv_from_gdrive(file_id):
    # url for GoogleDrive
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    response.raise_for_status()
    # Convert response text into a file-like object so pandas can read it
    csv_data = io.StringIO(response.text)
    df = pd.read_csv(csv_data)
    return df

# List of States & fileID
file_ids = {
    "PA": "1HPn-erywYpJgCmGseK7FKmwvcJzjEpTn",
    "IL": "1gn8ox4ugz6-917Myzl6o-rsWwYj5edab",
    "FL": "1R30A6cOrGveVkRhgmXemcPvlygqXuUfY",
    "TX": "18Eso9ZJhrwcN5Av0H7haZgQsgO2NOEQ8",
    "CA": "1uoFrXT2wQiBK63rOiVYxQs7NeiXAYhUR"
}

# List to store each state's DataFrame
df_list = []

# Loop over each state and file_id
for state, fid in file_ids.items():
    df_state = load_csv_from_gdrive(fid)
    df_list.append(df_state)

# Combine all DataFrames into one
df_combined = pd.concat(df_list, ignore_index=True)
keep_columns = ["Id", "BIRTHDATE", "DEATHDATE", "MARITAL", "RACE", "ETHNICITY", "GENDER", "CITY", "STATE", "COUNTY", "INCOME"]
patients_all = df_combined[keep_columns]

patients_all.to_csv("data/processed/patients_all.csv", index=False)

#explore the combined dataset
print(df_combined.head())
rows, cols = df_combined.shape
print("Number of rows:", rows)
print("Number of columns:", cols)
state_counts = df_combined['state'].value_counts()
print(state_counts)