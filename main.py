from utils.plots import *
from utils.data_reader import *

if __name__ == "__main__":
    counties_file_address = 'data/counties.json'
    covid_file_address = 'data/covid_deaths_usafacts.csv'

    covid_data, counties_data = read_data(covid_file_address, counties_file_address)

    covid_data, dates = clean_covid_data(covid_data)

    covid_data = reduce_data_columns(covid_data, dates, ['countyFIPS'])

    for date in dates:
        print('>>> Date: ' + date)
        plot_a_day(covid_data[['countyFIPS', date]], counties_data, date, show=False, save=True)

    # animate_over_time(covid_data, counties_data, dates[0:6])
