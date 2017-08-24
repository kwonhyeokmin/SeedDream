import openpyxl as ol
import pandas as pd
import re

# convert string to data
def convertDate(date):
    date = re.split('[. ]', date)
    date[-1] = date[-1].replace('(','')
    date[-1] = date[-1].replace(')','')
    return date
# if all values in list are None
# it return False.
# if not, it return True.
def isNoneRow(row):
    for cell in row:
        value = cell.value
        if value!=None:
            return True
    return False

# if row(tuple) has cell contained value
# it return True
def isContain(row, value):
    for v in row:
        if v.value==value:
            return True
    return False

def preprocess(path, isConverted):
    # if file is type of '생육조사자료'
    if isConverted:
        data = []
        date = [None for x in range(4)]
        book = ol.load_workbook(path)
        sheet = book.active
        rows = sheet.rows
        next(rows)
        next(rows)
        #next(rows)
        for row in rows:
            #생육조사일
            if isContain(row, '생육조사일'):
                date = row[15].value
                date = convertDate(date)
                continue
            # 작성자
            if isContain(row, '작성자'):
                continue
            # 속성값
            if isContain(row, '위치'):
                colum = list(x.value for x in row)
                columns = ['년', '월', '일', '요일']
                columns.extend(colum)
                continue
            if isNoneRow(row):
                values = list(x.value for x in row)
                date.extend(values)
                data.append(date.copy())
                date = [None for x in range(4)]

        df = pd.DataFrame(columns=columns, data=data)
        # replace a missing values
        df.ix[:, 0:8] = (df.ix[:, 0:8]).fillna(method='ffill') # replace with last value
        df.ix[:, 4:8] = (df.ix[:, 4:8]).fillna(0)  # replace with zero
        df.ix[:, 8:] = (df.ix[:, 8:]).fillna(0) # replace with zero
    else:
        df = pd.read_excel(path)
        df = df.fillna(0)
    return df
