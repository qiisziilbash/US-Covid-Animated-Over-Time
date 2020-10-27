import json

import pandas as pd
import plotly.express as px


def read_data(covid_address, counties_address):
    # read counties information
    # data is downloaded from : https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json
    print('>>> Reading counties data from: ' + counties_address)
    with open(counties_address, 'r') as fp:
        counties = json.load(fp)

    # read usa covid data by counties and date
    # you can download the updated version from:
    # https://static.usafacts.org/public/data/covid-19/covid_confirmed_usafacts.csv

    print('>>> Reading covid data from: ' + covid_address)
    covid = pd.read_csv(covid_address, dtype={"countyFIPS": str})

    return covid, counties


def process_covid_data(data):
    print('>>> Processing covid data ... ')
    # removing un-allocated cases
    data = data.drop(data[data.countyFIPS == '0'].index)
    data = data.reset_index()

    # padding county fips with left zeros
    data = pad_county_fips(data, 'countyFIPS')

    return data


def pad_county_fips(data, col_name):
    for index, row in data.iterrows():
        county_fips_length = len(data.loc[index, col_name])
        if county_fips_length < 5:
            data.loc[index, col_name] = '0' * (5 - county_fips_length) + row[col_name]
    return data


def plot_a_day(date, covid, counties):
    fig = px.choropleth(covid, geojson=counties, locations='countyFIPS', color='8/25/20',
                        color_continuous_scale="Burg",
                        range_color=(0, max(covid[date])),
                        scope="usa",
                        labels={'8/25/20': 'cases'}
                        )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


if __name__ == "__main__":

    counties_file_address = 'data/counties.json'
    covid_file_address = 'data/covid_confirmed_usafacts.csv'

    covid_data, counties_data = read_data(covid_file_address, counties_file_address)

    covid_data = process_covid_data(covid_data)

    plot_a_day('8/25/20', covid_data, counties_data)

