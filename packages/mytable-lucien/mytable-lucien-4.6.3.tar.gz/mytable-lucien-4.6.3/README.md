# MYTABLE
A simple package for processing data in the form of a table.

Pay attention, *all indexes start from 0 instead of 1*.

To install:
```shell
pip install mytable-lucien
```
To import:
```python
import mytable
```
## MYCSV
This is a simple reader and writer for CSV files by Lucien Shaw.
It consumes less resource and processes more quickly than the current csv module, though a lot less functional.

It reads CSV files as plain texts and stores the table in a list, whose elements are lists of cells of the current row. The list is the value to the key 'full' of a dict, which is the returned value of the function.

Here is the guidance.
### To import
```python
from mytable import mycsv
```
### Function: read()
Read a CSV file and store the table in a list.
- usage
```python
res = mycsv.read(filname, delimiter=',')
```
- arguments
  - filename
  
    A string value. The filename of the CSV file.
  - delimiter
  
    A char value. Comma by default. The character which is used to delimit the columns.
- returned value
  - res
      
    List of rows. Each row is a list of columns, aka. cells, which contains strings. 
### Function: write()
Create a CSV file.
- usage
```python
mycsv.write(filename, table, delimiter=',')
```
- arguments
  - filename
    
    A string value. The filename of the CSV file be written.
  - table
  
    A list, the structure of which is the same as the value to the key 'full' of the returned dict of function read().
    
    All values shall be **strings**.
  - delimiter
  
    A char value. Comma by default. The character which is used to delimit the columns.
- returned value

  There is no returned value.
## MYTOOLS
Useful tools. Simple, but powerful.
### To import
```python
from mytable import mytools
```
### Function: excel_ctn()
All functions of this package use numbers as indexes, but Excel uses alphabets as indications of the columns, such as 'A' for column 0 (*We count from 0, remember?*), 'Z' for column 25, and 'AA' for column 26.

This converts the alphabetical column Characters To pure Numbers.
- usage
```python
res = mytools.excel_ctn(col)
```
- arguments
  - col

    Alphabetical column characters, such as 'A' or 'AA', etc.
- returned value
  
  A number, as mentioned above.
## MYVIEW
Provide a better view of the tables.
### To import
```python
from mytable import myview
```
### Function: select_range()
In some circumstances, there are so many columns that they cannot be fully displayed in excel, and columns that exceed the limit cannot be visualized.

This allows you to select some columns and rows so that you can extract them to a new temporary CSV file and view them with your favorite table viewer, like Excel.
- usage
```python
table_select = myview.select_range(table, columns=[], rows=[])
```
- arguments
  - table

    An original table in the form of a list.
  - columns
  
    A list of column numbers that indicate the columns you would like to see. The default value is an empty list, which selects all columns.
  - rows

    A list of row numbers that indicate the rows you would like to see. The default value is an empty list, which selects all rows.
- returned value
  - table_select

    A table which contains the selected range. 
## MYEDIT
Edit the table the easy way.
### To import
```python
from mytable import myedit
```
### Function: combine_rows()
Combine rows of multiple tables with the same total number of columns.
- usage
```python
comb = myedit.combine_rows(tables)
```
- arguments
  - tables

    A list which contains multiple tables.
- returned value
  - comb
  
    The combined table.
### Function: combine_columns()
Combine columns of multiple tables with the same total number of rows.
- usage
```python
comb = myedit.combine_columns(tables)
```
- arguments
  - tables

    A list which contains multiple tables.
- returned value
  - comb
  
    The combined table.