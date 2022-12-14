from Connect import Connect
import matplotlib.pyplot as plt


class CaseTwo:
    def _init_(self, county):
        self.county = county
        self.all_time_id = []
        self.all_register = []
        self.connect = Connect('mdb')

    def view(self):
        statement = 'SELECT fips FROM county_dimension WHERE county_dimension.name = \'' + self.county + '\''
        table = self.connect.select(statement)
        if not table:
            return
        fips = int(table[0][0])
        statement = 'SELECT time_id FROM facts WHERE county_fips = ' + str(fips) + ' ORDER BY time_id ASC'
        table = self.connect.select(statement)
        for row in table:
            self.all_time_id.append(row[0])
        female_cases = []
        male_cases = []
        statement = 'SELECT female_cases, male_cases FROM facts WHERE county_fips = ' + str(
            fips) + ' ORDER BY time_id ASC'
        table = self.connect.select(statement)
        for row in table:
            female_cases.append(row[0])
            male_cases.append(row[1])

        fig, axs = plt.subplots(2, 1)
        axs[0].plot(self.all_time_id, female_cases)
        axs[0].set_xticks([])
        axs[0].set_xlabel('Tiempo')
        axs[0].set_ylabel('Cantidad de casos')
        axs[0].legend(title='Población femenina de ' + self.county.capitalize())

        axs[1].plot(self.all_time_id, male_cases)
        axs[1].set_xticks([])
        axs[1].set_xlabel('Tiempo')
        axs[1].set_ylabel('Cantidad de casos')
        axs[1].legend(title='Población masculina de ' + self.county.capitalize())

        plt.show()