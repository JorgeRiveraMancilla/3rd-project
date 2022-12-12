import configparser

from DataFrame import DataFrame
from MDB import MDB
from Connect import Connect


def init_dataframe():
    dataframe = DataFrame(states_us='resources/states_us.csv', daily_cases_us='resources/daily_cases_us.csv',
                          counties_us='resources/counties_us.csv')
    dataframe.transform()
    init_database(dataframe)


def init_database(dataframe):
    connect = Connect('mdb')
    connect.create_tables()
    mdb = MDB(dataframe.get_states_dataframe(),
              dataframe.get_daily_cases_dataframe(),
              dataframe.get_counties_dataframe(), connect)
    mdb.insert()


if __name__ == '__main__':
    init_dataframe()
