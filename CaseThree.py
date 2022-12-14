from Connect import Connect
import matplotlib.pyplot as plt


class CaseThree:
    def __init__(self, county):
        self.county = county

        self.years = []
        self.months = []

        self.max_female_cases = []
        self.min_female_cases = []

        self.max_male_cases = []
        self.min_male_cases = []

        self.connect = Connect('mdb')

    def view(self):
        statement = 'SELECT fips FROM county_dimension WHERE county_dimension.name = \'' + self.county + '\''
        table = self.connect.select(statement)
        if not table:
            return
        fips = int(table[0][0])

        statement = 'SELECT year, month FROM time_dimension GROUP BY year, month ORDER BY year, month ASC'
        table = self.connect.select(statement)
        for row in table:
            self.years.append(row[0])
            self.months.append(row[1])

        for i in range(len(self.years)):
            year = self.years[i]
            month = self.months[i]

            statement = 'SELECT MAX(female_cases), MIN(female_cases), MAX(male_cases), MIN(male_cases) FROM facts,' \
                        'time_dimension t WHERE time_id = t.id AND county_fips = ' + str(fips) + ' AND year = ' +\
                        str(year) + ' AND month = ' + str(month)
            table = self.connect.select(statement)

            self.max_female_cases.append(table[0][0] if table[0][0] is not None else 0)
            self.min_female_cases.append(table[0][1] if table[0][1] is not None else 0)
            self.max_male_cases.append(table[0][2] if table[0][2] is not None else 0)
            self.min_male_cases.append(table[0][3] if table[0][3] is not None else 0)

        months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

        for i in range(len(self.months)):
            self.months[i] = str(self.months[i]) + '/' + str(self.years[i])[2:]

        fig, axs = plt.subplots(2, 1)
        axs[0].plot(self.months, self.max_female_cases)
        axs[0].plot(self.months, self.min_female_cases)
        axs[0].set_ylabel('Cantidad de casos')
        axs[0].legend(title='Población femenina de ' + self.county.capitalize())

        axs[1].plot(self.months, self.max_male_cases)
        axs[1].plot(self.months, self.min_male_cases)
        axs[1].set_ylabel('Cantidad de casos')
        axs[1].legend(title='Población masculina de ' + self.county.capitalize())

        plt.show()
