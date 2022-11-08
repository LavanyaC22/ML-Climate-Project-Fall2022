#Preprocessing agricultural yield data

#Libraries
import pandas as pd

#import data
yield_data = pd.read_csv("Sweet_potato_yield_data.csv")
country_data = pd.read_csv("countries.csv")

countries = list(country_data["Country"])
result_dict = {"Country":[], "Year":[]}

for country in countries:
    for year in range(1961, 2021):
        result_dict["Country"].append(country)
        result_dict["Year"].append(year)

result_df = pd.DataFrame(result_dict)

#add all data to relevant columns 
for idx, row in yield_data.iterrows():
    result_df.loc[(result_df["Country"]==row["Area"]) & (result_df["Year"] == row["Year"]), row["Element"]] = row["Value"]

#export final data 
result_df.to_csv("Yield_data.csv")