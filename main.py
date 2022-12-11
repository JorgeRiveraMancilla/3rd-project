from DataFrame import DataFrame

# from Connect import Connect
# from RDB import RDB
# from MDB import MDB
# from Cube import Cube

if __name__ == '__main__':
    dataframe = DataFrame(states_us='resources/states_us.csv', daily_cases_us='resources/daily_cases_us.csv',
                          counties_us='resources/counties_us.csv')
    print(dataframe.to_string())
