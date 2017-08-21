import openpyxl as ol
import pandas as pd

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
    if isConverted:
        data = []
        book = ol.load_workbook(path)
        sheet = book.active
        rows = sheet.rows
        next(rows)
        next(rows)
        next(rows)
        for row in rows:
            #생육조사일
            if isContain(row, '생육조사일'):
                date = row[15].value
                continue
            # 작성자
            if isContain(row, '작성자'):
                continue
            # 속성값
            if isContain(row, '위치'):
                colum = list(x.value for x in row)
                continue
            if isNoneRow(row):
                value = list(x.value for x in row)
                data.append(value)

        df = pd.DataFrame(columns=colum, data=data)
        # replace a missing values
        df.ix[:, 0:4] = (df.ix[:, 0:4]).fillna(method='ffill') # replace with last value
        df.ix[:, 0:4] = (df.ix[:, 0:4]).fillna(0)  # replace with zero
        df.ix[:, 4:] = (df.ix[:, 4:]).fillna(0) # replace with zero
    else:
        df = pd.read_excel(path)
    return df

