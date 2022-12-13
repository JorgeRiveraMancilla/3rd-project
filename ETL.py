import pandas
from MDB import MDB
from RDB import RDB


class ETL:
    # region EXTRACT

    def __init__(self, paths, delimiters):
        self.df_states = pandas.read_csv(paths[0], delimiter=delimiters[0])
        self.df_counties = pandas.read_csv(paths[1], delimiter=delimiters[1])
        self.df_daily_cases = pandas.read_csv(paths[2], delimiter=delimiters[2])

    # endregion

    # region TRANSFORM

    def transform(self):
        self.df_states = self.__lower_case(self.df_states)
        self.df_counties = self.__lower_case(self.df_counties)
        self.df_daily_cases = self.__lower_case(self.df_daily_cases)

        self.df_daily_cases.dropna(subset=['fips'], inplace=True)
        self.df_daily_cases.fillna(value={'deaths': 0}, inplace=True)

        self.df_states = self.__remove_character(self.df_states, '\'', '')
        self.df_states = self.__remove_character(self.df_states, ' county', '')
        self.df_counties = self.__remove_character(self.df_counties, '\'', '')
        self.df_counties = self.__remove_character(self.df_counties, ' county', '')
        self.df_daily_cases = self.__remove_character(self.df_daily_cases, '\'', '')
        self.df_daily_cases = self.__remove_character(self.df_daily_cases, ' city', '')

        self.__rename_columns(self.df_counties, {'male': 'male_population',
                                                 'female': 'female_population',
                                                 'median_age': 'average_age',
                                                 'lat': 'latitude',
                                                 'long': 'longitude'})
        self.__rename_columns(self.df_daily_cases, {'cases': 'total_cases',
                                                    'cases_m': 'male_cases',
                                                    'cases_f': 'female_cases'})

        self.__fill_state_code(self.df_states, 'district of columbia', 'dc')
        self.__fill_state_code(self.df_states, 'puerto rico', 'pr')

        self.__fill_state_code(self.df_counties, 'district of columbia', 'dc')
        self.__fill_state_code(self.df_counties, 'puerto rico', 'pr')

        self.__check_state()
        self.__check_counties()
        self.__check_fips()

        # self.__check_population()
        # self.__check_cases()

    def __lower_case(self, df):
        df = df.applymap(lambda x: x.lower() if type(x) == str else x)
        return df.rename(columns=str.lower)

    def __remove_character(self, df, before, after):
        return df.apply(lambda x: x.astype(str).str.replace(before, after))

    def __rename_columns(self, df, new_columns):
        df.rename(columns=new_columns, inplace=True)

    def __fill_state_code(self, df, state_name, state_code):
        df.update(df['state_code'].mask(df['state'] == state_name, lambda x: state_code))

    def __check_state(self):
        errors = []
        states_in_counties_file = []
        for state in self.df_counties['state'].unique():
            if state not in states_in_counties_file:
                states_in_counties_file.append(state)
        for state in self.df_daily_cases['state'].unique():
            if state not in states_in_counties_file:
                errors.append(state)
        for state_error in errors:
            self.df_daily_cases = self.df_daily_cases[self.df_daily_cases['state'] != state_error]

    def __check_counties(self):
        errors = []
        counties_in_counties_file = []
        for county in self.df_counties['county'].unique():
            if county not in counties_in_counties_file:
                counties_in_counties_file.append(county)
        for county in self.df_daily_cases['county'].unique():
            if county not in counties_in_counties_file:
                errors.append(county)
        for county_error in errors:
            self.df_daily_cases = self.df_daily_cases[self.df_daily_cases['county'] != county_error]

    def __check_fips(self):
        errors = []
        fips_in_counties_file = []
        for fips in self.df_counties['fips'].unique():
            fips = float(fips)
            if fips not in fips_in_counties_file:
                fips_in_counties_file.append(fips)
        for fips in self.df_daily_cases['fips'].unique():
            fips = float(fips)
            if fips not in fips_in_counties_file:
                errors.append(fips)
        for fips_error in errors:
            self.df_daily_cases = self.df_daily_cases[self.df_daily_cases['fips'] != fips_error]

    def __check_population(self):
        errors = []
        df = pandas.merge(self.df_states, self.df_counties, how='outer', on=['county', 'state', 'state_code'])
        for index, row in df.iterrows():
            total_population = row[3]
            male_population = row[5]
            female_population = row[6]
            if total_population != male_population + female_population:
                fips = row[4]
                errors.append(fips)
        print(errors)

    def __check_cases(self):
        errors = []
        df = pandas.merge(self.df_counties, self.df_daily_cases, how='outer', on=['county', 'state', 'fips'])
        for index, row in df.iterrows():
            total_cases = row[10]
            male_cases = row[4]
            female_cases = row[5]
            if total_cases != male_cases + female_cases:
                fips = row[0]
                errors.append(fips)
        print(errors)

    # endregion

    # region LOAD

    def load(self):
        mdb = MDB(self.df_states, self.df_counties, self.df_daily_cases)
        mdb.insert()

        rdb = RDB(self.df_states, self.df_counties, self.df_daily_cases)
        rdb.insert()

    # endregion
