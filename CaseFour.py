from Connect import Connect
import matplotlib.pyplot as plt


class CaseFour:
    def __init__(self, state):
        self.state = state
        self.counties = []
        self.fips = []

        self.connect = Connect('mdb')

    def view(self):
        statement = 'SELECT code, c.fips FROM county_dimension c, state_dimension s WHERE c.state_code = code AND ' \
                    's.name = \'' + self.state + '\' ORDER BY c.fips ASC'
        table = self.connect.select(statement)
        if not table:
            return
        for row in table:
            self.counties.append(row[0])
            self.fips.append(row[1])
        cases_states = []
        for fips in self.fips:
            statement = 'SELECT female_cases, male_cases FROM facts WHERE ' \
                        'county_fips = ' + str(fips)
            table = self.connect.select(statement)
            cases_counties = []
            for row in table:
                cases_counties.append(row[0] + row[1])
            cases_states.append(cases_counties)

        plt.rcParams['figure.autolayout'] = True
        fig, ax = plt.subplots()
        ax.boxplot(cases_states)
        ax.set_xticks([])
        ax.set_title('Gráfico de cajas y bigotes de cada estado')
        plt.show()


