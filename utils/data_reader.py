import json
import pandas as pd


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


def clean_covid_data(data):
    print('>>> Processing covid data ... ')
    # removing un-allocated cases
    data = data.drop(data[data.countyFIPS == '0'].index)

    # dropping the index
    data = data.reset_index()
    data = data.drop(columns=['index'])

    # reformat damn American dates to international dates
    data, dates = reformat_dates(data)

    # padding county fips with left zeros
    data = pad_county_fips(data)

    return data, dates


def reformat_dates(data):
    col_names = data.columns.to_list()
    col_rename_dictionary = {}
    dates = []

    for name in col_names:
        if '/' in name:
            month = int(name.split('/')[0])
            day = int(name.split('/')[1])
            year = name.split('/')[2]

            new_date = '20' + year + '-' + f'{month:02d}' + '-' + f'{day:02d}'
            dates.append(new_date)

            col_rename_dictionary[name] = new_date

    data = data.rename(columns=col_rename_dictionary)

    return data, dates


def pad_county_fips(data):
    col_name = 'countyFIPS'

    for index, row in data.iterrows():
        county_fips_length = len(data.loc[index, col_name])
        if county_fips_length < 5:
            data.loc[index, col_name] = '0' * (5 - county_fips_length) + row[col_name]
    return data
