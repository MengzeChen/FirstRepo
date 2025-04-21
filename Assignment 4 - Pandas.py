import pandas as pd

# Step 1: Create dt1 - IFR per age based on Table 1 (CDC estimates)
ifr_by_age = []
for age in range(0, 101):
    if age <= 17:
        ifr = 20 / 1_000_000
    elif age <= 49:
        ifr = 500 / 1_000_000
    elif age <= 64:
        ifr = 6000 / 1_000_000
    else:
        ifr = 90000 / 1_000_000
    ifr_by_age.append((age, ifr))

ifr_df = pd.DataFrame(ifr_by_age, columns=["Age", "IFR"])

# Step 2: Read WorldDemographics.csv (dt2)
demographics_df = pd.read_csv("C:\\Users\\44821\\Desktop\\WorldDemographics.csv")

# Step 3: Clean up demographics data
demographics_df = demographics_df.rename(columns={"#Alive": "Population"})

# Step 4: Merge on Age
dt_merged = pd.merge(demographics_df, ifr_df, on="Age", how="inner")

# Step 5: Extract country name from PopulationID (e.g., 'United States_34' → 'United States')
dt_merged["Country"] = dt_merged["PopulationID"].str.extract(r"^([^_]+)")

# Step 6: Calculate expected deaths per row
dt_merged["Expected_Deaths"] = dt_merged["Population"] * dt_merged["IFR"]

# Step 7: Group by country to create summary
dt3 = dt_merged.groupby("Country").agg(
    Total_Population=("Population", "sum"),
    Total_Expected_Deaths=("Expected_Deaths", "sum")
).reset_index()

# Step 8: Calculate percentage died
dt3["Percent_Died"] = (dt3["Total_Expected_Deaths"] / dt3["Total_Population"]) * 100

# Step 9: Round for clarity
dt3["Total_Expected_Deaths"] = dt3["Total_Expected_Deaths"].round(2)
dt3["Percent_Died"] = dt3["Percent_Died"].round(4)

# Step 10: Save to CSV without index
dt3.to_csv("CountrySummary.csv", index=False)

# Preview first few rows
print(dt3.head())