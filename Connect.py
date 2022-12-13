import configparser
import psycopg2


class Connect:
    def __init__(self, database):
        config = configparser.ConfigParser()
        config.read('resources/config.ini')
        connection_info = config['database']
        self.database = connection_info[database]
        self.connect = psycopg2.connect(database=self.database,
                                        user=connection_info['user'],
                                        password=connection_info['password'],
                                        host=connection_info['server'],
                                        port=connection_info.getint('port'))

    def execute(self, query):
        cursor = self.connect.cursor()
        cursor.execute(query)
        cursor.close()
        self.connect.commit()

    def select(self, query):
        cursor = self.connect.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def create_tables(self):
        script = open('resources/' + self.database + '_schema.sql', mode='r').read()
        self.execute(script)

    def close(self):
        self.connect.close()
        del self.database
