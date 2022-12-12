import pandas


class DataFrame:
    __default_values = {
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
        self.__dataframes = dict()
        # **kwargs replace key-value array with csv path and their names,
        # thus we don't need a paired key-value data structure to assign in the class dict
        for key, value in kwargs.items():
            self.__populate_dictionary(key, value)

    def __populate_dictionary(self, file_name, path_file):
        # Finds type of dataframe and delimit each one
        if path_file == 'resources/states_us.csv':
            self.__dataframes[file_name] = pandas.read_csv(path_file, delimiter=',')
        elif path_file == 'resources/daily_cases_us.csv':
            self.__dataframes[file_name] = pandas.read_csv(path_file, delimiter=',')
        elif path_file == 'resources/counties_us.csv':
            self.__dataframes[file_name] = pandas.read_csv(path_file, delimiter='/')
        else:
            raise ValueError("The path_file: '%s' is not in the class list" % path_file)

    def transform(self):
        # Se pide que se coloquen respectivos upper y lower case
        self.__generic_normalize_dataframe()
        # llama a la normalización especifica de cada dataframe
        self.__specific_normalize()
        # valida los fips irregulares de daily cases
        # verifica que las poblaciones coincidan entre states_us y counties_us
        self.__verify_population()

    # region GENERIC NORMALIZATION
    def __generic_normalize_dataframe(self):
        self.__word_case_typer()
        self.__rename_columns()

    def __word_case_typer(self):
        for dataframe in self.__dataframes:
            self.__dataframes[dataframe] = \
                self.__dataframes[dataframe]\
                    .applymap(lambda value: value.upper().replace("'", "") if type(value) == str else value)
            self.__dataframes[dataframe].rename(columns=str.lower, inplace=True)

    def __rename_columns(self):
        for dataframe in self.__dataframes.values():
            dataframe.rename(
                columns={'state_code': 'code', 'male': 'male_population',
                         'female': 'female_population',
                         'median_age': 'average_age', 'lat': 'latitude', 'long': 'longitude', 'cases_m': 'male_cases',
                         'cases_f': 'female_cases', 'cases': 'total_cases'}, inplace=True)

    # endregion

    # region SPECIFIC NORMALIZATION
    def __specific_normalize(self):
        self.__normalize_daily_cases_dataframe()
        self.__normalize_states_us_dataframe()
        self.__normalize_counties_us_dataframe()

    def __normalize_counties_us_dataframe(self):
        data_frame = self.__dataframes['counties_us']
        data_frame.update(data_frame['code'].mask(data_frame['state'] == "DISTRICT OF COLUMBIA", lambda x: 'DC'))
        data_frame.update(data_frame['code'].mask(data_frame['state'] == "PUERTO RICO", lambda x: 'PR'))

    def __normalize_states_us_dataframe(self):
        data_frame = self.__dataframes['states_us']
        data_frame.update(data_frame['code'].mask(data_frame['state'] == "DISTRICT OF COLUMBIA", lambda x: 'DC'))
        data_frame.update(data_frame['code'].mask(data_frame['state'] == "PUERTO RICO", lambda x: 'PR'))

    def __normalize_daily_cases_dataframe(self):
        self.__dataframes['daily_cases_us']['date'] = self.__dataframes['daily_cases_us']['date'].str.replace('!%', '/')
        self.__dataframes['daily_cases_us'] = self.__dataframes['daily_cases_us'][
            self.__dataframes['daily_cases_us'].county != 'UNKNOWN']
        self.__dataframes['daily_cases_us']['deaths'] = self.__dataframes['daily_cases_us']['deaths'].fillna('NULL')
        self.__manage_irregular_fips()
        self.__drop_unknown_values()

    # region NORMALIZE_DAILY_CASES
    def __manage_irregular_fips(self):
        data_frame = self.__dataframes['daily_cases_us']
        data_frame.update(data_frame['fips'].mask(data_frame['county'] == "NEW YORK CITY", lambda x: 36061))
        data_frame.update(data_frame['fips'].mask(data_frame['county'] == "KANSAS CITY", lambda x: 29095))

    def __drop_unknown_values(self):
        data_frame = self.__dataframes['daily_cases_us']
        index = data_frame[(data_frame['county'] == 'unknown')].index
        data_frame.drop(index, inplace=True)

    # endregion

    # endregion

    # region VERIFIY_POPULATION
    def __verify_population(self):
        # REVISAR!
        merge_dataframe = pandas.merge(self.__dataframes['counties_us'], self.__dataframes['states_us'], how="outer")
        merge_dataframe['suma población'] = merge_dataframe.iloc[:, [4, 5]].sum(axis=1)
        # get the sum of the columns "male" and "female" and check if is equal to "population" of the county
        for i in merge_dataframe.index:
            if merge_dataframe['population'][i] != merge_dataframe['suma población'][i]:
                print("The county with different population is : ", merge_dataframe['county'][i])
        print("All data related with population and sum of people by genre is okay")

    # endregion

    # region GETTERS
    def get_states_dataframe(self):
        return self.__dataframes['states_us']

    def get_counties_dataframe(self):
        return self.__dataframes['counties_us']

    def get_daily_cases_dataframe(self):
        return self.__dataframes['daily_cases_us']

    # endregion

    # region OBJECT_OVERRIDES
    def __repr__(self):
        string_builder = ""
        for dataframe in self.__dataframes.values():
            string_builder += dataframe.__repr__() + "\n"
        return string_builder
    # endregion
