import Util


class MDB:

    def __init__(self, states, daily_cases, counties, connect):
        self.states = states
        self.daily_cases = daily_cases
        self.counties = counties
        self.connect = connect

    def insert(self):
        # self.__insert_states()
        self.__insert_counties()
        self.__insert_time()
        self.__insert_faks()

    def __insert_states(self):
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

    def __insert_counties(self):
        pass

    def __insert_time(self):
        for date in self.daily_cases['date'].unique():
            items = date.split('/')
            statement = Util.insert_statement('time_dimension',
                                              ['register', 'year', 'month', 'day'],
                                              ["'" + date + "'",  str(items[0]), str(items[1]), str(items[2])])
            self.connect.execute(statement)

    def __insert_faks(self):
        pass
