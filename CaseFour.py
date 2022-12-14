from Connect import Connect
import matplotlib.pyplot as plt


class CaseFour:
    def __init__(self, state):
        self.state = state
        self.counties = []
        self.fips = []

        self.connect = Connect('mdb')

    def view(self):
        statement = 'SELECT c.name, c.fips FROM county_dimension c, state_dimension s WHERE c.state_code = code AND ' \
                    's.name = \'' + self.state + '\''
        table = self.connect.select(statement)
        if not table:
            return
        for row in table:
            self.counties.append(row[0])
            self.fips.append(row[1])




