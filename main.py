import configparser
from ETL import ETL
from Cube import Cube
from CaseOne import CaseOne
from CaseTwo import CaseTwo
from CaseThree import CaseThree
from CaseFour import CaseFour

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('resources/config.ini')

    if config['program'].getboolean('etl'):
        paths = config['paths']
        etl = ETL([paths['path_file_states'], paths['path_file_counties'], paths['path_file_daily_cases']],
                  [',', '/', ','])
        etl.transform()
        etl.load()

    cube = Cube()

    if config['program'].getboolean('case_one'):
        case_one = CaseOne()
        case_one.view()

    if config['program'].getboolean('case_two'):
        case_two = CaseTwo('autauga')
        case_two.view()

    if config['program'].getboolean('case_three'):
        case_three = CaseThree('autauga')
        case_three.view()

    if config['program'].getboolean('case_four'):
        case_four = CaseFour('alabama')
        case_four.view()
