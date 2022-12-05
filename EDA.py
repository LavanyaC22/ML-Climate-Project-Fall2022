#Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Load data file
df = pd.read_csv("yield_and_climate_data.csv")

#Dataset info
df.info()

## Data cleaning

#Dealing with missing values - remove rows without yield data and/or climate data
df.dropna(axis = 0, how = "any", inplace = True)
# df.info()

# ## Summary statistics
# print(df.describe().round(2))

# #Data points by year and by country
# print(df.groupby("Year").count())
# print(df.groupby("Country").count())


#Dummy varibles for countries
d_df = pd.get_dummies(df, columns = ["Country"])

# ## Distribution of vatiables
# d_df.iloc[:, 2:88].hist(figsize=(12,8),bins=20)
# plt.show()

# ## Multivariate analysis
# plt.figure(figsize=(10,6))
# sns.pairplot(d_df.iloc[:, 2:88])
# plt.show()

# ## Correlation map
# plt.figure(figsize=(10,6))
# sns.heatmap(df.corr(),annot=True)
# plt.show()


# #inspecting all time trend of all variables
# def get_all_time_variable_trends(country, variables):
#     #create plot
#     fig, axs = plt.subplots(nrows=len(variables), ncols=1)
#     #add title
#     fig.suptitle('Trends for '+country)
#     #collect data from dataframe
#     for i in range(len(variables)):
#         var_x = []
#         var_y = []    
#         years = df.loc[df["Country"] == country, "Year"]
#         for year in years:
#             for month in list(['01', '02', '03','04', '05', '06','07', '08', '09','10', '11', '12']):
#                 var_x.append(month+str(year))
#                 var_y.append(df.loc[(df["Country"] == country) & (df["Year"] == year), variables[i]+"_"+month].iloc[0])
#         #add data to plots
#         axs[i].plot(var_x, var_y)
#         axs[i].title.set_text(variables[i])
#     plt.show()
            
# #inspecting annual trend of all variables
# def get_annual_variable_trends(country, year, variables):
#     #create plot
#     fig, axs = plt.subplots(nrows=len(variables), ncols=1)
#     #add title
#     fig.suptitle('Trends for '+country)
#     #collect data from dataframe
#     for i in range(len(variables)):
#         var_x = []
#         var_y = []    
#         for month in list(['01', '02', '03','04', '05', '06','07', '08', '09','10', '11', '12']):
#             var_x.append(month)
#             var_y.append(df.loc[(df["Country"] == country) & (df["Year"] == year), variables[i]+"_"+month].iloc[0])
#         #add data to plots
#         axs[i].plot(var_x, var_y)
#         axs[i].title.set_text(variables[i])
#     plt.show()


variables = ['cloud_cover', 'snow_thickness_lwe', 'snow_thickness', 'vapour_pressure',
                '2m_temperature', '10m_wind_speed', '2m_dewpoint_temperature']
# get_all_time_variable_trends("United States of America", variables)
# get_annual_variable_trends("United States of America", 2020, variables)

months = ['01', '02', '03','04', '05', '06','07', '08', '09','10', '11', '12']

#Aggregate monthly data into 3 month groups and annually
for variable in variables:
    for i in range(4):
        d_df[variable+"_g"+str(i)] = d_df[[variable+"_"+months[3*i], variable+"_"+months[3*i+1], variable+"_"+months[3*i+2]]].mean(axis=1) 
    d_df[variable] = d_df[[variable+"_g0", variable+"_g1", variable+"_g2", variable+"_g3"]].mean(axis= 1)

d_df.to_csv("yield_and_climate_data_cleaned.csv", index = False)