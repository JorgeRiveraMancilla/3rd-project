import configparser
from DataFrame import DataFrame
#from Connect import Connect
#from RDB import RDB
#from MDB import MDB
#from Cube import Cube


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('resources/config.ini')
    paths = config['paths']
    if config['database'].getboolean('normalize'):
        dataframe_1 = DataFrame(paths['path_file_counties_us'])
        dataframe_1.normalize()
        dataframe_2 = DataFrame(paths['path_file_states_us'])
        dataframe_2.normalize()
        dataframe_3 = DataFrame(paths['path_file_daily_cases_us'])
        dataframe_3.normalize()

        print(dataframe_1.dataframe)
        print(dataframe_2.dataframe)
        print(dataframe_3.dataframe)
