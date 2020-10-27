import calendar
import os

import numpy as np
import plotly.express as px


def reduce_data_columns(data, dates, columns):
    columns.extend(dates)
    return data[columns]


def transform_cases_for_day_plot(data, date):
    data['Cases (Log10)'] = np.log10(data[date] + 1)
    data = data.rename(columns={date: 'Cases'})
    return data


def get_string_cases(cases):
    if cases <= 10:
        return '<b>' + str(cases) + '</b>'
    elif cases < 100:
        return '<b>' + '< ' + str(round(np.floor(cases/10) * 10)) + '</b>'
    elif cases < 1000:
        return '<b>' + '< ' + str(round(np.floor(cases / 100) * 100)) + '</b>'
    elif cases < 900000:
        return '<b>' + '< ' + str(round(np.floor(cases / 1000))) + 'k' + '</b>'
    else:
        return '<b>' + str(cases) + '</b>'


def reformat_date(date):
    day = int(date.split('-')[2])
    month = calendar.month_name[int(date.split('-')[1])]
    year = date.split('-')[0]

    day_bar = ''
    for i in range(day):
        day_bar += '◉'

    for i in range(max(calendar.monthrange(int(year), int(date.split('-')[1]))) - day):
        day_bar += '⊙'

    return '<b>' + month + ' ' + year + '</b>' + '<br>' + '<b>' + day_bar + '</b>'


def get_colorbar_ticks(max_tick, count):
    tick_values = []
    tick_texts = []

    ticks = np.logspace(0, max_tick, num=count)

    if max(ticks) < count - 1:
        for i in range(round(10 ** max_tick - 1) + 1):
            tick_values.append(np.log10(i + 1))
            tick_texts.append(round(i))
    else:
        for i in np.logspace(0, max_tick, num=count):
            tick_values.append(np.log10(i + 1))
            tick_texts.append(get_string_cases(round(i)))

    return tick_values, tick_texts


def plot_a_day(covid, counties, date, show, save):
    covid = transform_cases_for_day_plot(covid, date)

    fig = px.choropleth(covid,
                        geojson=counties,
                        locations='countyFIPS',
                        color='Cases (Log10)',
                        hover_data=['Cases'],
                        color_continuous_scale="PiYG_r",
                        range_color=(0, max(covid['Cases (Log10)'])),
                        scope="usa",
                        title=reformat_date(date),
                        )

    tick_vals, tick_texts = get_colorbar_ticks(max(covid['Cases (Log10)']), 5)

    fig.update_layout(title_x=0.5, title_font_family="Times New Roman", title_font_size=30,
                      coloraxis_colorbar=dict(
                          title='',
                          tickvals=tick_vals,
                          ticktext=tick_texts,
                          tickfont=dict(
                              color='black',
                              size=25
                          )
                      ))
    if show:
        fig.show()
    if save:
        if not os.path.exists('images'):
            os.mkdir('images')

        fig.write_image('images/' + date + '.png', width=2*1080, height=2*720)


def transform_cases_for_animation(covid, dates):
    cols = dates.extend('countyFIPS')
    covid = covid[cols]
    covid = covid.melt(id_vars=['countyFIPS'], var_name='Date', value_name='Cases')
    covid['Cases (Log10 scale)'] = np.log10(covid['Cases'] + 1)

    return covid


def animate_over_time(covid, counties, dates):
    covid = transform_cases_for_animation(covid, dates)

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