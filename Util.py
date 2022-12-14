def select_statement(tables, conditions):
    statement = 'SELECT * FROM '
    n = len(tables)
    for i in range(n - 1):
        statement += tables[i] + ', '
    if conditions is None:
        return statement + tables[n - 1]
    statement += tables[n - 1] + ' WHERE '
    n = len(conditions)
    for i in range(n - 1):
        statement += conditions[i] + ' AND '
    return statement + conditions[n - 1]


def insert_statement(table, columns, values):
    start = 'INSERT INTO ' + table + '('
    end = ') VALUES ('
    n = len(columns)
    for i in range(n - 1):
        start += columns[i] + ', '
        end += values[i] + ', '
    return start + columns[n - 1] + end + values[n - 1] + ')'
