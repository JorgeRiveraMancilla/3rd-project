import Util


class MDB:

    def __init__(self, states, daily_cases, counties, connect):
        self.states = states
        self.daily_cases = daily_cases
        self.counties = counties
        self.connect = connect

    def insert(self):
        self.__insert_states()
        self.__insert_counties()
        self.__insert_time()
        self.__insert_facts()

    def __insert_states(self):
        self.__insert_nonexistent_states()
        for row in self.states[['state', 'code']].iterrows():
            name = "'" + str(row[1][0]) + "'"
            code = "'" + str(row[1][1]) + "'"
            statement = Util.select_statement(['state_dimension'], ['code = ' + code, 'name = ' + name])
            table = self.connect.select(statement)
            if not table:
                statement = Util.insert_statement('state_dimension',
                                                  ['code', 'name'],
                                                  [code, name])
                self.connect.execute(statement)

    def __insert_nonexistent_states(self):
        statement = Util.insert_statement('state_dimension',
                                          ['code', 'name'],
                                          ["'VI'", "'ST. CROIX ISLAND'"])
        self.connect.execute(statement)

    def __insert_counties(self):
        self.__insert_nonexistent_counties()
        for row in self.counties[['fips', 'county', 'code', 'male_population', 'female_population',
                                  'latitude', 'longitude']].iterrows():
            fips = str(row[1][0])
            county = "'" + str(row[1][1]) + "'"
            code = "'" + str(row[1][2]) + "'"
            male_population = str(row[1][3])
            female_population = str(row[1][4])
            total_population = str(int(row[1][3]) + int(row[1][4]))
            latitude = str(row[1][5])
            longitude = str(row[1][6])
            self.__execute_insert_county_query(fips, county, male_population, female_population, total_population,
                                               latitude, longitude, code)

    def __insert_nonexistent_counties(self):
        virgin_island_counties = [[78010, 'ST. CROIX', 24592, 26009, 50601, 17.746639, -64.703201, 'VI'],
                                  [78020, 'ST. JOHN', 2027, 2143, 4170, 18.3368, 64.7281, 'VI'],
                                  [78030, 'ST. THOMAS', 25094, 26540, 51634, 18.3368, 64.7281, 'VI']]
        for row in virgin_island_counties:
            fips = str(row[0])
            county = "'" + str(row[1]) + "'"
            male_population = str(row[2])
            female_population = str(row[3])
            total_population = str(row[4])
            latitude = str(row[5])
            longitude = str(row[6])
            code = "'" + str(row[7]) + "'"
            self.__execute_insert_county_query(fips, county, male_population, female_population, total_population,
                                               latitude, longitude, code)

    def __execute_insert_county_query(self, fips, county, male_population, female_population, total_population,
                                      latitude, longitude, code):
        statement = Util.select_statement(['county_dimension'], ['fips = ' + fips])
        table = self.connect.select(statement)
        if not table:
            statement = Util.insert_statement('county_dimension',
                                              ['fips', 'name', 'male_population', 'female_population',
                                               'total_population', 'latitude', 'longitude', 'state_code'],
                                              [fips, county, male_population, female_population, total_population,
                                               latitude, longitude, code])
            self.connect.execute(statement)

    def __insert_time(self):
        for date in self.daily_cases['date'].unique():
            items = date.split('/')
            statement = Util.insert_statement('time_dimension',
                                              ['register', 'year', 'month', 'day'],
                                              ["'" + date + "'",  str(items[0]), str(items[1]), str(items[2])])
            self.connect.execute(statement)

    def __insert_facts(self):
        decidoserfeliz = []
        for row in self.daily_cases[['male_cases', 'female_cases', 'total_cases', 'deaths', 'fips', 'date']].iterrows():
            male_cases = str(row[1][0])
            female_cases = str(row[1][1])
            total_cases = str(row[1][2])
            deaths = str(row[1][3])
            fips = str(row[1][4])
            date = "'" + str(row[1][5]) + "'"
            statement = Util.select_statement(['time_dimension'], ['register = ' + date])
            table = self.connect.select(statement)
            time_id = str(table[0][0])
            statement = Util.select_statement(['county_dimension'], ['fips = ' + fips])
            table = self.connect.select(statement)
            if table:
                statement = Util.insert_statement(
                    'facts',
                    ['male_cases', 'female_cases', 'total_cases', 'deaths', 'county_fips', 'time_id'],
                    [male_cases, female_cases, total_cases, deaths, fips, time_id])
                self.connect.execute(statement)
            else:
                decidoserfeliz.append(fips)
        print()
