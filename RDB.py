import Util
from Connect import Connect


class RDB:
    def __init__(self, df_states, df_counties, df_daily_cases):
        self.df_states = df_states
        self.df_counties = df_counties
        self.df_daily_cases = df_daily_cases
        self.connect = Connect('rdb')
        self.connect.create_tables()

    def insert(self):
        self.__insert_states()
        self.__insert_counties()
        self.__insert_daily_cases()
        self.connect.close()

    def __insert_states(self):
        for index, row in self.df_states[['state', 'state_code']].iterrows():
            name = '\'' + str(row[0]) + '\''
            code = '\'' + str(row[1]) + '\''
            statement = Util.select_statement(['states'],
                                              ['code = ' + code])
            table = self.connect.select(statement)
            if not table:
                statement = Util.insert_statement('states',
                                                  ['code', 'name'],
                                                  [code, name])
                self.connect.execute(statement)

    def __insert_counties(self):
        for index, row in self.df_counties[['fips', 'county', 'state_code', 'male_population', 'female_population',
                                            'average_age', 'latitude', 'longitude']].iterrows():
            fips = str(row[0])
            name = '\'' + str(row[1]) + '\''
            male_population = str(row[3])
            female_population = str(row[4])
            average_age = str(row[5])
            latitude = str(row[6])
            longitude = str(row[7])
            state_code = '\'' + str(row[2]) + '\''
            statement = Util.select_statement(['counties'],
                                              ['fips = ' + fips])
            table = self.connect.select(statement)
            if not table:
                statement = Util.insert_statement('counties',
                                                  ['fips', 'name', 'male_population', 'female_population',
                                                   'average_age', 'latitude', 'longitude', 'state_code'],
                                                  [fips, name, male_population, female_population, average_age,
                                                   latitude, longitude, state_code])
                self.connect.execute(statement)

    def __insert_daily_cases(self):
        for index, row in self.df_daily_cases[['date', 'fips', 'deaths', 'male_cases', 'female_cases']].iterrows():
            county_fips = str(row[1])
            register = '\'' + str(row[0]) + '\''
            male_cases = str(row[3])
            female_cases = str(row[4])
            deaths = str(row[2])
            statement = Util.insert_statement('daily_cases',
                                              ['county_fips', 'register', 'male_cases', 'female_cases', 'deaths'],
                                              [county_fips, register, male_cases, female_cases, deaths])
            self.connect.execute(statement)
