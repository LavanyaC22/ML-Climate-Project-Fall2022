import cdsapi

c = cdsapi.Client()

c.retrieve(
    'sis-agrometeorological-indicators',
    {
        'format': 'zip',
        'variable': '2m_temperature',
        'statistic': '24_hour_mean',
        'year': '2020',
        'month': '01',
        'day': '01',
    },
    'download.zip')