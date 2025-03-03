import pandas as pd
#import matplotlib.pyplot as plt

patients_all = pd.read_csv(r"data/processed/patients_all.csv")
medications = pd.read_csv(r"data/processed/medications.csv")
conditions = pd.read_csv(r"data/processed/conditions.csv")
immunizations = pd.read_csv(r"data/processed/immunizations.csv")
observations = pd.read_csv(r"data/processed/observations.csv")
allergies = pd.read_csv(r"data/processed/allergies.csv")

###################
#  Patients all   #
###################

# Rename to match the others
patients_all.rename(columns={"Id": "PATIENT"}, inplace=True)

###################
#  Observations   #
###################
#clean what will become variables
observations["clean_desc"] = observations["DESCRIPTION"].astype(str).str.strip().str.lower().str.replace(r'\W+', '_',
                                                                                                         regex=True)
f_wide_observations = observations.pivot_table(
    index="PATIENT",
    columns="clean_desc",
    values="VALUE",
    aggfunc='first'  # only 1 already but keeping it here
).reset_index()

#they need to be numeric
for col in f_wide_observations.columns:
    if col != "PATIENT":
        f_wide_observations[col] = pd.to_numeric(f_wide_observations[col], errors='coerce')

###################
#  Allergies      #
###################
allergies["clean_desc"] = allergies["DESCRIPTION"].astype(str).str.strip().str.lower().str.replace(r'\W+', '_',
                                                                                                   regex=True)
allergies["has_allergy"] = 1
df_allergies_wide = allergies.pivot_table(
    index="PATIENT",
    columns="DESCRIPTION",
    values="has_allergy",
    aggfunc="max",  # 1 remains 1
    fill_value=0  # Fill missing values with 0
).reset_index()

###################
#  medications    #
###################
medications["clean_desc"] = medications["DESCRIPTION"].astype(str).str.strip().str.lower().str.replace(r'\W+', '_',
                                                                                                           regex=True)
medications["has_med"] = 1
df_medications_wide = medications.pivot_table(
    index="PATIENT",
    columns="DESCRIPTION",
    values="has_med",
    aggfunc="max",  # 1 remains 1
    fill_value=0  # Fill missing values with 0
).reset_index()

###################
#  immunizations  #
###################
immunizations["clean_desc"] = immunizations["DESCRIPTION"].astype(str).str.strip().str.lower().str.replace(r'\W+', '_',
                                                                                                           regex=True)
immunizations["has_imm"] = 1
df_immunizations_wide = immunizations.pivot_table(
    index="PATIENT",
    columns="DESCRIPTION",
    values="has_imm",
    aggfunc="max",  # 1 remains 1
    fill_value=0  # Fill missing values with 0
).reset_index()


merged_df = patients_all.copy()
# Merge the observations dataset
merged_df = merged_df.merge(f_wide_observations, on="PATIENT", how="left")
# Merge the allergies dataset
merged_df = merged_df.merge(df_allergies_wide, on="PATIENT", how="left")
# Merge the medications dataset
merged_df = merged_df.merge(df_medications_wide, on="PATIENT", how="left")
# Merge the immunizations dataset
merged_df = merged_df.merge(df_immunizations_wide, on="PATIENT", how="left")
# Merge the conditions dataset
merged_df = merged_df.merge(conditions, on="PATIENT", how="left")

obs_cols = f_wide_observations.columns.tolist()
cols_to_fill = [col for col in merged_df.columns if col not in obs_cols]
merged_df[cols_to_fill] = merged_df[cols_to_fill].fillna(0)

#patients with no record in the conditions dataset, fill cvd_flag with False.
merged_df["cvd_flag"] = merged_df["cvd_flag"].fillna(False)

#split 80% test, 20% train.
shuffled_df = merged_df.sample(frac=1, random_state=42).reset_index(drop=True)
train_size = int(0.8 * len(shuffled_df))
train_df = shuffled_df.iloc[:train_size]
test_df = shuffled_df.iloc[train_size:]

train_df.to_csv("data/processed/train.csv", index=False)
test_df.to_csv("data/processed/test.csv", index=False)