import pandas as pd

# Create the IFR DataFrame
ifr_by_age = []
age_ifr_pairs = [
    (range(0, 5), 0.00001),
    (range(5, 10), 0.00001),
    (range(10, 15), 0.00001),
    (range(15, 20), 0.00002),
    (range(20, 25), 0.0001),
    (range(25, 30), 0.0002),
    (range(30, 35), 0.0003),
    (range(35, 40), 0.0005),
    (range(40, 45), 0.001),
    (range(45, 50), 0.002),
    (range(50, 55), 0.004),
    (range(55, 60), 0.008),
    (range(60, 65), 0.015),
    (range(65, 70), 0.03),
    (range(70, 75), 0.06),
    (range(75, 80), 0.1),
    (range(80, 101), 0.2),
]

for age_range, ifr in age_ifr_pairs:
    for age in age_range:
        ifr_by_age.append((age, ifr))

ifr_df = pd.DataFrame(ifr_by_age, columns=["Age", "IFR"])

# Read in the Demographics CSV file
demographics_df = pd.read_csv("C:\\Users\\44821\\Desktop\\WorldDemographics.csv")

# Join the two DataFrames on the 'Age' column
merged_df = pd.merge(demographics_df, ifr_df, on="Age", how="inner")

# Print shape and columns of the merged DataFrame
print("New DataFrame shape:", merged_df.shape)
print("Columns:", merged_df.columns.tolist())

# Create a new column for expected deaths
merged_df["Expected_Deaths"] = merged_df["#Alive"] * merged_df["IFR"]

# Save the result (without the index column) to a new CSV
if "Unnamed: 0" in merged_df.columns:
    merged_df = merged_df.drop(columns=["Unnamed: 0"])

merged_df.to_csv("Joined_Demographics_IFR.csv", index=False)
