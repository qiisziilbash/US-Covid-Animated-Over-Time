import pandas as pd
from urllib.request import urlopen
import json

# get USA counties information
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


file_address = 'data/covid_confirmed_usafacts.csv'
covid_dataset = pd.read_csv(file_address)

print('hi')