import json
import os

import pandas as pd
import numpy as np
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


def plot_a_day(covid, counties, date, show, save):
    covid = transform_covid_for_day_plot(covid, date)

    fig = px.choropleth(covid,
                        geojson=counties,
                        locations='countyFIPS',
                        color='Cases (Log10)',
                        hover_data=['Cases'],
                        color_continuous_scale="PuRd",
                        range_color=(0, max(covid['Cases (Log10)'])),
                        scope="usa",
                        title=date,
                        )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    if show:
        fig.show()
    if save:
        if not os.path.exists('images'):
            os.mkdir('images')

        fig.write_image('images/' + date + '.png')


def reduce_data_columns(data, dates, columns):
    columns.extend(dates)
    return data[columns]


def transform_covid_for_day_plot(covid, date):
    covid['Cases (Log10)'] = np.log10(covid[date] + 1)
    covid = covid.rename(columns={date: 'Cases'})
    return covid


def transform_covid_for_animation(covid, dates):
    cols = dates.extend('countyFIPS')
    covid = covid[cols]
    covid = covid.melt(id_vars=['countyFIPS'], var_name='Date', value_name='Cases')
    covid['Cases (Log10 scale)'] = np.log10(covid['Cases'] + 1)

    return covid


def animate_over_time(covid, counties, dates):
    covid = transform_covid_for_animation(covid, dates)

    fig = px.choropleth(covid,
                        geojson=counties,
                        locations='countyFIPS',
                        color="Cases (Log10 scale)",
                        animation_frame="Date",
                        color_continuous_scale="PuRd",
                        scope="usa",
                        hover_data=['Cases'],
                        range_color=(0, max(covid['Cases (Log10 scale)'])),
                        title='Covid over time',
                        )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


if __name__ == "__main__":
    counties_file_address = 'data/counties.json'
    covid_file_address = 'data/covid_confirmed_usafacts.csv'

    covid_data, counties_data = read_data(covid_file_address, counties_file_address)

    covid_data, dates = clean_covid_data(covid_data)

    covid_data = reduce_data_columns(covid_data, dates, ['countyFIPS'])

    for date in dates:
        print('>>> Date: ' + date)
        plot_a_day(covid_data[['countyFIPS', date]], counties_data, date, show=False, save=True)

    # animate_over_time(covid_data, counties_data, dates[0:6])
