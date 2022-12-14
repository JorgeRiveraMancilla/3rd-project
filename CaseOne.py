import matplotlib.pyplot as plt
from matplotlib import gridspec
import pandas
from pandas.plotting import scatter_matrix


class CaseOne:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def view(self):
        self.__process()

    def __process(self):
        pandas.plotting.scatter_matrix(self.dataframe.convert_dtypes(convert_string=False), alpha=0.2)
