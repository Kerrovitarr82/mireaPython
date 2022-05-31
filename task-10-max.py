def delete_duplicate_columns(table):
    for row in table:
        del row[3]
        del row[3]
    return table


def split_col(table):
    for row in table:
        var = row[1].split('#')
        row[0] = str(int(float(var[0]) * 100)) + '%'
        if var[1] == 'Да':
            row[1] = 'Y'
        elif var[1] == 'Нет':
            row[1] = 'N'
    return table


def transform(table):
    for row in table:
        row[3] = row[3].replace(' ', '(', 1)
        row[3] = row[3].replace(' ', ')', 1)
        buf = row[2].split('-')
        buf[0] = buf[0][2:4]
        row[2] = buf[2] + '/' + buf[1] + '/' + buf[0]
    return table


def main(table):
    table = delete_duplicate_columns(table)
    table = split_col(table)
    table = transform(table)
    return table


table1 = [
    [None, '0.7#Да', '2001-05-22', None, '2001-05-22', '+7 824 169-29-11'],
    [None, '0.9#Да', '2004-06-01', None, '2004-06-01', '+7 599 189-86-69'],
    [None, '0.4#Нет‚', '1999-03-02', None, '1999-03-02', '+7 018 725-91-82']
]

print(main(table1))
