import configparser
from ETL import ETL


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('resources/config.ini')
    if config['database'].getboolean('etl'):
        paths = config['paths']
        etl = ETL([paths['path_file_states'], paths['path_file_counties'], paths['path_file_daily_cases']],
                  [',', '/', ','])
        etl.transform()
