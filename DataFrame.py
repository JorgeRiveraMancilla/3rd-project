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
            self.dataframes[file_name].applymap(lambda value: value.lower() if type(value) == str else value)
        self.dataframes[file_name].rename(
            columns=str.upper, inplace=True)

    def __normalize(self):
        self.__normalize_daily_cases_dataframe()
        pass

    def __normalize_daily_cases_dataframe(self):
        self.dataframes['daily_cases_us']['DATE'] = self.dataframes['daily_cases_us']['DATE'].str.replace('!%', '/')
        # Actually is not a useful code, it's only to verifier some inconsistent csv data
        for column in self.dataframes['daily_cases_us'].columns:
            if 'unknown' in set(self.dataframes['daily_cases_us'][column]):
                print("column: %s" % column)

# if 'date' in self.dataframe.columns:
#     self.dataframe['date'] = self.dataframe['date'].str.replace('!%', '/')
#     self.dataframe = self.dataframe[self.dataframe.county != 'UNKNOWN']
#     self.dataframe['deaths'] = self.dataframe['deaths'].fillna('NULL')

# if self.dataframe.iloc[319]['county'] == "DISTRICT OF COLUMBIA":
#     self.dataframe.loc[319, 'state_code'] = "DC"
#     self.dataframe[['state_code']] = self.dataframe[['state_code']].fillna('PR')

    def verify_population(self):
        if not self.file_exists:
            raise FileNotFoundError
        self.dataframe['suma población'] = self.dataframe.iloc[:, [4, 5]].sum(axis=1)
        # print(self.dataframe)
        for i in self.dataframe.index:
            if self.dataframe['population'][i] != self.dataframe['suma población'][i]:
                print("The county with different population is : ", self.dataframe['name'][i])
                return False

    def to_string(self):
        for dataframe in self.dataframes.values():
            print(dataframe)
