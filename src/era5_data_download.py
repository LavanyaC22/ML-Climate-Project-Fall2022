import cdsapi
import pandas as pd

c = cdsapi.Client()

countries = pd.read_csv("countries.csv")
yield_data = pd.read_csv("yield_data_by_country.csv")

variables = [
                'cloud_cover', 'snow_thickness_lwe', 'snow_thickness', 'vapour_pressure',
                '2m_temperature', '10m_wind_speed', '2m_dewpoint_temperature'
            ]
# years = [
#                     '1979', '1980', '1981',
#                     '1982', '1983', '1984',
#                     '1985', '1986', '1987',
#                     '1988', '1989', '1990',
#                     '1991', '1992', '1993',
#                     '1994', '1995', '1996',
#                     '1997', '1998', '1999',
#                     '2000', '2001', '2002',
#                     '2003', '2004', '2005',
#                     '2006', '2007', '2008',
#                     '2009', '2010', '2011',
#                     '2012', '2013', '2014',
#                     '2015', '2016', '2017',
#                     '2018', '2019', '2020',
#                 ]

for country in list(countries["Country"]):
  years = list(yield_data.loc[yield_data["Country"] == country, "Year"])
    for variable in variables:
        for year in years:
            if int(year) >= 1979 and int(year) <= 2020:
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
