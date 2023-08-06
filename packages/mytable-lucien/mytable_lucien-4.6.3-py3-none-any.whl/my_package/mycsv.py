def read(filname,has_header,delimiter=','):
    res = {
        'full': [],
        'data': [],
        'has_header': bool(has_header),
        'columns': 0,
        'rows': 0,
        'rows_data': 0,
    }
    with open(filname, 'r') as f:
        table = f.readlines()
    for row in table:
        res['full'].append(row.strip('\n').split(delimiter))
    if has_header:
        res['data'] = res['full'][1:]
    else:
        res['data'] = res['full'][:]
    res['columns'] = len(res['full'][0])
    res['rows'] = len(res['full'])
    res['rows_data'] = len(res['data'])
    return res
def write(filename,table,delimiter=','):
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
        
