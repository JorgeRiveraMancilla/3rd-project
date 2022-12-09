import configparser
import pandas

class DataFrame:
    dict = {
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

    def __init__(self, path_file):
        try:
            if path_file == "resources/counties_us.csv":
                self.dataframe = pandas.read_csv(path_file, delimiter='/')
            else:
                self.dataframe = pandas.read_csv(path_file)
            self.file_exists = True

        except FileNotFoundError:
            self.file_exists = False

    def normalize(self):
        if not self.file_exists:
            raise FileNotFoundError

        self.dataframe.columns = self.dataframe.columns.str.lower()

        if 'state' in self.dataframe.columns:
            self.dataframe['state'] = self.dataframe['state'].str.upper()

        if 'county' in self.dataframe.columns:
            self.dataframe['county'] = self.dataframe['county'].str.upper()

        if 'date' in self.dataframe.columns:
            self.dataframe['date'] = self.dataframe['date'].str.replace('!%', '/')
            self.dataframe = self.dataframe[self.dataframe.county != 'UNKNOWN']
            self.dataframe['deaths'] = self.dataframe['deaths'].fillna('NULL')

        if 'fips' in self.dataframe.columns:
            self.dataframe['fips'] = self.dataframe['fips'].astype(str)

        if self.dataframe.iloc[319]['county'] == "DISTRICT OF COLUMBIA":
            self.dataframe.loc[319, 'state_code'] = "DC"
            self.dataframe[['state_code']] = self.dataframe[['state_code']].fillna('PR')

        self.dataframe.rename(
            columns={'state_code': 'code', 'county': 'name', 'male': 'male_population', 'female': 'female_population',
                     'median_age': 'average_age', 'lat': 'latitude', 'long': 'longitude', 'cases_m': 'male_cases',
                     'cases_f': 'female_cases'}, inplace=True)

    def verify_population(self):
        if not self.file_exists:
            raise FileNotFoundError
        self.dataframe['suma población'] = self.dataframe.iloc[:, [4, 5]].sum(axis=1)
        #print(self.dataframe)
        for i in self.dataframe.index:
            if self.dataframe['population'][i] != self.dataframe['suma población'][i]:
                print("The county with different population is : ",self.dataframe['name'][i])
                return False
