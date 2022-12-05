#Pre-processing climate data downloaded from AgERA5
#loop over all files - country, variable, year
#unzip folder, for each day and each point in grid, aggregate to get monthly stat for region
#add data to dataframe

import xarray as xr
import numpy as np
import os
from zipfile import ZipFile
import pandas as pd
import re
import shutil

df = pd.read_csv("Yield_data.csv")

countries = pd.read_csv("countries.csv")
variables = [
                'cloud_cover', 'snow_thickness_lwe', 'snow_thickness', 'vapour_pressure',
                '2m_temperature', '10m_wind_speed', '2m_dewpoint_temperature'
            ]
years = [
            '1979', '1980', '1981',
            '1982', '1983', '1984',
            '1985', '1986', '1987',
            '1988', '1989', '1990',
            '1991', '1992', '1993',
            '1994', '1995', '1996',
            '1997', '1998', '1999',
            '2000', '2001', '2002',
            '2003', '2004', '2005',
            '2006', '2007', '2008',
            '2009', '2010', '2011',
            '2012', '2013', '2014',
            '2015', '2016', '2017',
            '2018', '2019', '2020',
        ]
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
for m in months:
    df = df.reindex(columns = df.columns.tolist() + [v + "_" + m for v in variables])

for country in list(countries["Country"]):
    for variable in variables:
        for year in years:
            folder_name = country+"_"+variable+"_"+year
            #unzip folder
            with ZipFile(folder_name + ".zip", 'r') as zObject:
                zObject.extractall(path=folder_name)
                zObject.close()
            #from new folder, read all NC files
            monthly_var = {}
            for filename in os.listdir(folder_name):
                f = os.path.join(folder_name,filename)
                if os.path.isfile(f):
                    ds = xr.open_mfdataset(f)
                    month = re.findall(re.compile(r"AgERA5_"+year +"(.{2})"),f)[0]
                    #since for all variables, we take the mean to downscale
                    #take the mean of values over all longitudes and latitudes                 
                    if month not in monthly_var:
                        monthly_var[month] = []
                    monthly_var[month].append(np.nanmean(np.array(ds.variables[np.array(ds.variables)[-1]])))
            #aggregate over month to get monthly average value of variable and store in 
            for month, v in monthly_var.items():
                df.loc[(df["Country"]==country) & (df["Year"] == int(year)), variable+"_"+month] = np.mean(v)

df.to_csv("yield_and_climate_data.csv")
