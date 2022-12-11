from DataFrame import DataFrame

# from Connect import Connect
# from RDB import RDB
# from MDB import MDB
# from Cube import Cube

# I've working on DataFrame class so temporally this block of code will not run
# def allan_method():
#
#     config = configparser.ConfigParser()
#     config.read('resources/config.ini')
#     paths = config['paths']
#     if config['database'].getboolean('normalize'):
#         dataframe_1 = DataFrame(paths['path_file_counties_us'])
#         dataframe_1.normalize()
#         dataframe_2 = DataFrame(paths['path_file_states_us'])
#         dataframe_2.normalize()
#         dataframe_3 = DataFrame(paths['path_file_daily_cases_us'])
#         dataframe_3.normalize()
#
#         merge_dataframe = pd.merge(dataframe_1.dataframe, dataframe_2.dataframe, how="outer")
#         merge_dataframe.to_csv("resources/merge.csv", index=False, encoding='utf-8-sig')
#         verify_Dataframe = DataFrame(paths['path_file_merge'])
#         verify_Dataframe.verify_population()
#         print(dataframe_1.dataframe)
#         print(dataframe_2.dataframe)
#         print(dataframe_3.dataframe)


if __name__ == '__main__':
    dataframe = DataFrame(states_us='resources/states_us.csv', daily_cases_us='resources/daily_cases_us.csv',
                          counties_us='resources/counties_us.csv')
    # print(dataframe.to_string())
