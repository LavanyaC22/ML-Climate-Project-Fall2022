#Preprocessing agricultural yield data

#Libraries
import pandas as pd

#import data
yield_data = pd.read_csv("Sweet_potato_yield_data.csv")
region_data = pd.read_csv("regions.csv")
country_data = pd.read_csv("countries.csv")

#clean up regions dataframe
region_data.loc[region_data["Country"] == 'United States of America\xa0', "Country"] = "United States of America"

countries = list(country_data["Country"])
regions = list(region_data["Region"])

result_dict_country = {"Country":[], "Year":[]}
result_dict_region = {"Region":[], "Year":[], "Country":[]}

#add rows corresponding to country, year and region to dataframes
for year in range(1961, 2021):  
    for country in countries:
        result_dict_country["Country"].append(country)
        result_dict_country["Year"].append(year)
    for region in regions:
        result_dict_region["Region"].append(region)
        result_dict_region["Year"].append(year)
        result_dict_region["Country"].append(region_data.loc[region_data["Region"] == region, "Country"].iloc[0])


result_df_country = pd.DataFrame(result_dict_country)
result_df_region = pd.DataFrame(result_dict_region)
result_df_region["Production"] = ''
result_df_region["Area harvested"] = ''
result_df_region["Yield"] = ''

#add all data to relevant columns 
#for country level data
for idx, row in yield_data.iterrows():
    result_df_country.loc[(result_df_country["Country"]==row["Area"]) & (result_df_country["Year"] == row["Year"]), row["Element"]] = row["Value"]

#for region level data
for idx, row in result_df_region.iterrows():
    perc = region_data.loc[(region_data["Region"]==row["Region"]), "Percentage"].iloc[0]
    for val in ["Production", "Area harvested", "Yield"]:
        result_df_region.at[idx, val] = perc*(result_df_country.loc[(result_df_country["Country"]==row["Country"]) & (result_df_country["Year"]==row["Year"]), val]).iloc[0]


#remove empty rows
result_df_region.dropna(axis = 0, how = "any", inplace = True)
result_df_country.dropna(axis = 0, how = "any", inplace = True)

#export final data 
result_df_country.to_csv("yield_data_by_country.csv", index = False)
result_df_region.to_csv("yield_data_by_region.csv", index = False)