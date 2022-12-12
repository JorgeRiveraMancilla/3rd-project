import pandas


class DataFrame:
    default_values = {
        'fips': False,
        'date': False,
        'state': 'CONSTRUCTOR',
        'state_code': 'CONSTRUCTOR',
        'male': False,
        'female': False,
        'median_age': 'NULL',
        'county': False,
        'cases': 'NULL',
        'deaths': False,
        'population': False,
        'cases_m': False,
        'cases_f': False,
    }

    def __init__(self, **kwargs: str):
        # First create the minimum class attributes to work
        self.dataframes = dict()
        # **kwargs replace key-value array with csv path and their names,
        # thus we don't need a paired key-value data structure to assign in the class dict
        for key, value in kwargs.items():
            self.__populate_dictionary(key, value)
            self.__word_case_typer(key)
        self.__normalize()
        self.verify_population()
        self.rename_columns()

    def __populate_dictionary(self, file_name, path_file):
        # Finds type of dataframe and delimit each one
        if path_file == 'resources/states_us.csv':
            self.dataframes[file_name] = pandas.read_csv(path_file, delimiter=',')
        elif path_file == 'resources/daily_cases_us.csv':
            self.dataframes[file_name] = pandas.read_csv(path_file, delimiter=',')
        elif path_file == 'resources/counties_us.csv':
            self.dataframes[file_name] = pandas.read_csv(path_file, delimiter='/')
        else:
            raise ValueError("The path_file: '%s' is not in the class list" % path_file)

    def __word_case_typer(self, file_name):
        self.dataframes[file_name] = \
            self.dataframes[file_name].applymap(lambda value: value.upper() if type(value) == str else value)
        self.dataframes[file_name].rename(
            columns=str.lower, inplace=True)

    def __normalize(self):
        self.__normalize_daily_cases_dataframe()
        self.__normalize_states_us_dataframe()
        self.__normalize_counties_us_dataframe()
        pass

    def __normalize_counties_us_dataframe(self):
        if self.dataframes['counties_us'].loc[319]['county'] == "DISTRICT OF COLUMBIA":
            self.dataframes['counties_us'].loc[319, 'state_code'] = "DC"
            self.dataframes['counties_us']['state_code'] = self.dataframes['counties_us']['state_code'].fillna('PR')

    def __normalize_states_us_dataframe(self):
        if self.dataframes['states_us'].loc[319]['county'] == "DISTRICT OF COLUMBIA":
            self.dataframes['states_us'].loc[319, 'state_code'] = "DC"
            self.dataframes['states_us']['state_code'] = self.dataframes['states_us']['state_code'].fillna('PR')

    def __normalize_daily_cases_dataframe(self):
        self.dataframes['daily_cases_us']['date'] = self.dataframes['daily_cases_us']['date'].str.replace('!%', '/')
        self.dataframes['daily_cases_us'] = self.dataframes['daily_cases_us'][
            self.dataframes['daily_cases_us'].county != 'UNKNOWN']
        self.dataframes['daily_cases_us']['deaths'] = self.dataframes['daily_cases_us']['deaths'].fillna('NULL')

        # Actually is not a useful code, it's only to verifier some inconsistent csv data
        for column in self.dataframes['daily_cases_us'].columns:
            if 'unknown' in set(self.dataframes['daily_cases_us'][column]):
                print("column: %s" % column)

    def verify_population(self):
        merge_dataframe = pandas.merge(self.dataframes['counties_us'], self.dataframes['states_us'], how="outer")
        merge_dataframe['suma población'] = merge_dataframe.iloc[:, [4, 5]].sum(axis=1)
        # print(merge_dataframe)
        # merge_dataframe.to_csv("merge.csv", index=False, encoding='utf-8-sig')

        # get the sum of the columns "male" and "female" and check if is equal to "population" of the county
        for i in merge_dataframe.index:
            if merge_dataframe['population'][i] != merge_dataframe['suma población'][i]:
                print("The county with different population is : ", merge_dataframe['county'][i])
        print("All data related with population and sum of people by genre is okay")

    def rename_columns(self):
        for dataframe in self.dataframes.values():
            dataframe.rename(
                columns={'state_code': 'code', 'county': 'name', 'male': 'male_population',
                         'female': 'female_population',
                         'median_age': 'average_age', 'lat': 'latitude', 'long': 'longitude', 'cases_m': 'male_cases',
                         'cases_f': 'female_cases'}, inplace=True)

    def __repr__(self):
        string_builder = ""
        for dataframe in self.dataframes.values():
            string_builder += dataframe.__repr__() + "\n"
        return string_builder
