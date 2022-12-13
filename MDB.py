import Util
from Connect import Connect


class MDB:
    def __init__(self, df_states, df_counties, df_daily_cases):
        self.df_states = df_states
        self.df_counties = df_counties
        self.df_daily_cases = df_daily_cases
        self.connect = Connect('mdb')
        self.connect.create_tables()

    def insert(self):
        self.__insert_states()
        self.__insert_counties()
        self.__insert_time()
        self.__insert_facts()
        self.connect.close()

    def __insert_states(self):
        for index, row in self.df_states[['state', 'state_code']].iterrows():
            name = '\'' + str(row[0]) + '\''
            code = '\'' + str(row[1]) + '\''
            statement = Util.select_statement(['state_dimension'],
                                              ['code = ' + code])
            table = self.connect.select(statement)
            if not table:
                statement = Util.insert_statement('state_dimension',
                                                  ['code', 'name'],
                                                  [code, name])
                self.connect.execute(statement)

    def __insert_counties(self):
        for index, row in self.df_counties[['fips', 'county', 'state_code', 'male_population', 'female_population',
                                            'latitude', 'longitude']].iterrows():
            fips = str(row[0])
            name = '\'' + str(row[1]) + '\''
            male_population = str(row[3])
            female_population = str(row[4])
            total_population = str(int(row[3]) + int(row[4]))
            latitude = str(row[5])
            longitude = str(row[6])
            state_code = '\'' + str(row[2]) + '\''
            statement = Util.select_statement(['county_dimension'],
                                              ['fips = ' + fips])
            table = self.connect.select(statement)
            if not table:
                statement = Util.insert_statement('county_dimension',
                                                  ['fips', 'name', 'male_population', 'female_population',
                                                   'total_population', 'latitude', 'longitude', 'state_code'],
                                                  [fips, name, male_population, female_population, total_population,
                                                   latitude, longitude, state_code])
                self.connect.execute(statement)

    def __insert_time(self):
        for register in self.df_daily_cases['date'].unique():
            items = register.split('!%')
            register = '\'' + register + '\''
            statement = Util.insert_statement('time_dimension',
                                              ['register', 'year', 'month', 'day'],
                                              [register, str(items[0]), str(items[1]), str(items[2])])
            self.connect.execute(statement)

    def __insert_facts(self):
        for index, row in self.df_daily_cases[['male_cases', 'female_cases', 'total_cases', 'deaths', 'fips',
                                               'date']].iterrows():
            male_cases = str(row[0])
            female_cases = str(row[1])
            total_cases = str(row[2])
            deaths = str(row[3])
            county_fips = str(row[4])
            register = '\'' + str(row[5]) + '\''
            statement = Util.select_statement(['time_dimension'], ['register = ' + register])
            table = self.connect.select(statement)
            time_id = str(table[0][0])
            statement = Util.insert_statement(
                'facts',
                ['male_cases', 'female_cases', 'total_cases', 'deaths', 'county_fips', 'time_id'],
                [male_cases, female_cases, total_cases, deaths, county_fips, time_id])
            self.connect.execute(statement)
