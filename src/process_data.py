"""
Reading the data from GoogleDrive
"""

#import necessary packages
import pandas as pd
import numpy as np
import requests
import io

#Patients dataset
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

#Convert BIRTHDATE column to a datetime type
df_combined["BIRTHDATE"] = pd.to_datetime(df_combined["BIRTHDATE"])
df_combined["DEATHDATE"] = pd.to_datetime(df_combined["DEATHDATE"])
df_combined["BIRTHDATE_ORD"] = df_combined["BIRTHDATE"].apply(lambda d: d.toordinal())

#Define a function that calculates age at death
def calc_age_at_death(row):
    birth = row["BIRTHDATE"]
    death = row["DEATHDATE"]
    if pd.isnull(death):
        return np.nan
    return (death - birth).days // 365
df_combined["AGE_AT_DEATH"] = df_combined.apply(calc_age_at_death, axis=1)


keep_columns = ["Id", "BIRTHDATE", "BIRTHDATE_ORD", "DEATHDATE", "AGE_AT_DEATH", "MARITAL", "RACE", "ETHNICITY", "GENDER", "CITY", "STATE", "COUNTY", "INCOME"]
patients_all = df_combined[keep_columns]

patients_all.to_csv("data/processed/patients_all.csv", index=False)

#Conditions

# List of States & fileID for conditions
file_ids = {
    "PA": "1xeuzrlJ8PeeV_UYAdKuS0-SWZP4iW_zc",
    "IL": "1697EYEVyhmkFTME7LMkJiMOFeZmapf4q",
    "FL": "1-HvfZFniBsjbnepdH4apquD3nXeQ8KlQ",
    "TX": "17zzvVVcXt8uhKr8_h9J-1MeDZAb1C5Pe",
    "CA": "1k4a4sKSHUyUjR2kQu-lObJC8ggpJ3Y3d"
}
# List to store each state's DataFrame
df_list = []
# Loop over each state and file_id
for state, fid in file_ids.items():
    df_state = load_csv_from_gdrive(fid)
    df_list.append(df_state)
# Combine all DataFrames into one
df_combined = pd.concat(df_list, ignore_index=True)

# Keeping only heart related conditions
pattern = r"heart|cardio|myocardial|coronary|angina|cardiac"
df_combined["cvd_flag"] = df_combined["DESCRIPTION"].str.contains(pattern, case=False, na=False)

# Group by PATIENT so that if any condition is True for that patient, the result is True.
df_patient_flag = df_combined.groupby("PATIENT")["cvd_flag"].any().reset_index()

df_patient_flag.to_csv("data/processed/conditions.csv", index=False)
