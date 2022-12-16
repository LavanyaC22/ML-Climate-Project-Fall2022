#Pre-processing climate data downloaded from AgERA5
#loop over all files - country, variable, year
#unzip folder, for each day and each point in grid, aggregate to get monthly stat for region
#add data to dataframe

#Import Libraries
import xarray as xr
import numpy as np
import os
from zipfile import ZipFile
import pandas as pd
import re
import shutil
from shapely import geometry 
import geopandas as gpd

#Load data

#country level
countries = pd.read_csv("countries.csv")
yield_data_by_country = pd.read_csv("yield_data_by_country.csv")
country_result = yield_data_by_country

#region level
# regions_df = pd.read_csv("regions.csv")
# yield_data_by_region = pd.read_csv("yield_data_by_region.csv")
# region_result = yield_data_by_region

#convert WKT object to GeoSeries object
# regions_df['geometry'] = gpd.GeoSeries.from_wkt(regions_df['Polygon_shape'])

variables = [
                'cloud_cover', 'snow_thickness', 'vapour_pressure',
                '2m_temperature', '10m_wind_speed', '2m_dewpoint_temperature'
            ]
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

#add columns representing monthly aggregates of all variables
for m in months:
    country_result = country_result.reindex(columns = country_result.columns.tolist() + [v + "_" + m for v in variables])
# for m in months:
#     region_result = region_result.reindex(columns = region_result.columns.tolist() + [v + "_" + m for v in variables])

countries_list = list(countries["Country"])

#at country level
for country in countries_list:
    years = list(yield_data_by_country.loc[yield_data_by_country["Country"] == country, "Year"])
    for variable in variables:
        for year in years:
            #constraining year based on available climate data
            if year >= 1979 and year <= 2020:
                folder_name = country+"_"+variable+"_"+ str(year)
                #unzip folder
                with ZipFile(country + "/" + folder_name + ".zip", 'r') as zObject:
                    zObject.extractall(path=folder_name)
                    zObject.close()
                #from new folder, read all NC files
                monthly_var = {}
                for filename in os.listdir(folder_name):
                    f = os.path.join(folder_name,filename)
                    print(filename)
                    if os.path.isfile(f):
                        ds = xr.open_mfdataset(f)
                        month = re.findall(re.compile(r"AgERA5_"+str(year) +"(.{2})"),f)[0]
                        #since for all variables, we take the mean to downscale
                        #take the mean of values over all longitudes and latitudes                 
                        if month not in monthly_var:
                            monthly_var[month] = []
                        monthly_var[month].append(np.nanmean(np.array(ds.variables[np.array(ds.variables)[-1]])))
                #aggregate over month to get monthly average value of variable and store in 
                for month, v in monthly_var.items():
                    country_result.loc[(df["Country"]==country) & (country_result["Year"] == int(year)), variable+"_"+month] = np.mean(v)

#storing result as csv                  
country_result.to_csv("yield_and_climate_data2.csv", index= False)


#at region level
# for country in countries_list:
#     #move into country folder
#     region_list = list(regions_df.loc[regions_df["Country"] == country, "Region"])
#     years = list(yield_data_by_country.loc[yield_data_by_country["Country"] == country, "Year"])
#     for variable in variables:
#         for year in years:
#             #constraining year based on available climate data
#             if year >= 1979 and year <= 2020:
#                 folder_name = country + "_" + variable + "_" + str(year)
#                 #unzip folders in folder
#                 with ZipFile(country + "/" +folder_name + ".zip", "r") as zObject:
#                     zObject.extractall(path=folder_name)
#                     zObject.close()
#                 #from new folder, read all NC files
#                 region_monthly_var = {}
#                 for region in region_list:
#                     region_monthly_var[region] = {}
#                     for month in months:
#                         region_monthly_var[region][month] = []
#                 for filename in os.listdir(folder_name):
#                     f = os.path.join(folder_name,filename)
#                     if os.path.isfile(f):
#                         ds = xr.open_mfdataset(f)
#                         cur_month = re.findall(re.compile(r"AgERA5_"+str(year) +"(.{2})"),f)[0]
#                         #since for all variables, we take the mean to downscale
#                         #take the mean of values over all longitudes and latitudes
#                         #loop over regions in the country to find values in the region  
#                         region_cur_mon_var_temp = {}
#                         for region in region_list:
#                             region_cur_mon_var_temp[region] = []
#                         #loop over all x and y coordinates
#                         #if point in region, then add it to region list
#                         for x in ds.variables['lon']:
#                             for y in ds.variables['lat']:
#                                 pt = geometry.Point(x, y)
#                                 for region in region_list:
#                                     polygon = regions_df.loc[regions_df["Region"] == region, "geometry"].iloc[0]
#                                     if polygon.contains(pt):
#                                         s = ds.sel(lon = x, method = "nearest").sel(lat = y, method = "nearest")
#                                         region_cur_mon_var_temp[region].append(float(s.variables[np.array(s.variables)[-1]]))
#                         #after checking all coordinates, aggregate the average for coordinates found
#                         for region in region_list:
#                             if len(region_cur_mon_var_temp[region]) != 0:
#                                 region_monthly_var[region][cur_month].append(np.nanmean(region_cur_mon_var_temp[region]))
#                 #aggregate over month to get monthly average value of variable and store in df
#                 for region, mon_v in region_monthly_var.items():
#                     for month, v in mon_v.items():
#                         if len(v) != 0:
#                             region_result.loc[(region_result["Region"]==region) & (region_result["Year"] == int(year)), variable+"_"+month] = np.mean(v)

#storing result as csv
# region_result.to_csv("yield_and_climate_data_by_region.csv", index= False)
