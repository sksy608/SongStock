###################################################################
# Derive from trading-stock-thailand/datasets/web_set_income.py
# sk 2018-12-17
# Objective to retrieve financial data from yahoo finance page
# Sample from PTT.BK as a Ticker
# 1. Income Statement Annually
# https://finance.yahoo.com/quote/PTT.BK/financials?p=PTT.BK
# 2. Income statement Quartery
# span = Quartery
# 3. Balance Sheet Annually
# https://finance.yahoo.com/quote/PTT.BK/balance-sheet?p=PTT.BK
# Method 1. getTableData, 2. createDataFrame, 3. writeCSVFile
#           4. writeCSVFile, 5. removeOldFile
###################################################################

import urllib2
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from os.path import join, exists
from os import  remove, makedirs

DIR_SEC_CSV = "sec_set_income"

def getTableData(symbol,finTyp):
    # There are 1. symbol, Income Statement, Annually
    #           2. symbol, Income Statement, Quartery
    #           3. symbol, Balance Sheet, Annually
    #           4. symbol, Balance Sheet, Quartery
    #           5. symbol, Cash Flow, Annually
    #           6. symbol, Cash Flow, Quartery
    if finTyp == 'BS':
        typ = 'balance-sheet'
    elif finTyp == 'CF':
        typ = 'cash-flow'
    else:
        typ = 'financials'

    url_string = "https://finance.yahoo.com/quote/"
    url_string += symbol
    url_string += "/"
    url_string += typ
    url_string += "?p="
    url_string += symbol

    response = urllib2.urlopen(url_string)
    page = response.read()
    soup = BeautifulSoup(page,'lxml')
    table_element = soup.findAll('table', class_='Lh(1.7) W(100%) M(0)')
    return table_element[len(table_element)-1]

def createDataFrame(table_element):
    #Generate lists
    row_list =[]
    index_list = []

    if table_element is None:
        return None

    num_col = 5
    count = 0

    # cut the row that have member less than 5 that have colspan="5" :sk
    for row5 in table_element.findAll("td", colspan="5"):
        row5.decompose()

    for row in table_element.findAll("td"):
        txt = row.find(text=True)
        count = count + 1
        if count % num_col == 1:
            txt = txt.replace('-', '*')
            index_list.append(txt)
        else:
            row_list.append(txt)

    # skip 'Statement of Comprehensive Income (MB.) and 'more'
    # index_list = index_list[1:len(index_list)-1]

    # skip first row :sk
    index_list = index_list[1:len(index_list)]

    num_col_df = num_col-1
    shape_row = len(row_list)/num_col_df
    row_list = np.reshape(row_list, (shape_row,num_col_df))

    all_head = row_list[0]
    all_row = row_list[1:]
    df = pd.DataFrame(columns = all_head, index = index_list, data = all_row)
    return df


# def writeCSVFile(df, symbol, output_path=DIR_SEC_CSV, include_index = False):
def writeCSVFile(df, symbol, typ, output_path=DIR_SEC_CSV, include_index = False):
    csv_file = "{}.csv".format(join(output_path, symbol + '-' + typ))
    # df.to_csv(csv_file, index = include_index)
    df.to_csv(csv_file, index = include_index, encoding='utf-8')

def removeOldFile(symbol, typ, output_path=DIR_SEC_CSV):
    csv_file = "{}.csv".format(join(output_path, symbol + '-' + typ))
    if exists(output_path) == False:
        makedirs(output_path)
    if exists(csv_file):
        remove(csv_file)

if __name__ == '__main__':

    table_element = getTableData('PTT.BK', 'IS')

    df = createDataFrame(table_element)
    print(df)

    removeOldFile('PTT.BK', 'IS') # clear old
    writeCSVFile(df, 'PTT.BK', 'IS', include_index = True)
