def read(filname, delimiter=','):
    res = []
    with open(filname, 'r', encoding = 'utf-8') as f:
        table = f.readlines()
    for row in table:
        res.append(row.strip('\n').split(delimiter))
    return res
def write(filename, table, delimiter=','):
    rows = len(table)
    columns = len(table[0])
    with open(filename, 'w', encoding = 'utf-8') as f:
        for row in range(rows):
            for column in range(columns):
                print(table[row][column],end='',file=f)
                if column < columns-1:
                    print(delimiter,end='',file=f)
            if row < rows-1:
                print('\n',end='',file=f)