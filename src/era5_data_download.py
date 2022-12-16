#Importing Libraries
import cdsapi
import pandas as pd

c = cdsapi.Client()

#Loading data 
countries = pd.read_csv("countries.csv")
yield_data = pd.read_csv("yield_data_by_country.csv")

variables = [
                'cloud_cover', 'snow_thickness', 'vapour_pressure',
                '2m_temperature', '10m_wind_speed', '2m_dewpoint_temperature'
            ]

for country in list(countries["Country"]):
    #requesting climate data for only those years crop production and yield data is available
    years = list(yield_data.loc[yield_data["Country"] == country, "Year"])
    for variable in variables:
        for year in years:
            #constraining years based on AgERA5 limits
            if int(year) >= 1979 and int(year) <= 2020:
                print(country, variable, year)
                c.retrieve(
                    'sis-agrometeorological-indicators',
                    {
                        'format': 'zip',
                        'variable': variable,
                        'statistic': '24_hour_mean',
                        'year': str(year),
                        'month':  [
                            '01', '02', '03',
                            '04', '05', '06',
                            '07', '08', '09',
                            '10', '11', '12',
                        ],
                        'day': [
                            '01', '02', '03',
                            '04', '05', '06',
                            '07', '08', '09',
                            '10', '11', '12',
                            '13', '14', '15',
                            '16', '17', '18',
                            '19', '20', '21',
                            '22', '23', '24',
                            '25', '26', '27',
                            '28', '29', '30',
                            '31',
                        ],
                        'area': [
                            int(countries.loc[countries["Country"] == country, "North"]), 
                            int(countries.loc[countries["Country"] == country, "West"]), 
                            int(countries.loc[countries["Country"] == country, "South"]), 
                            int(countries.loc[countries["Country"] == country, "East"]), 
                        ],
                    },
                    country+"_"+variable+"_"+str(year)+".zip")