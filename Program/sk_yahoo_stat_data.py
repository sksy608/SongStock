###################################################################
# Derive from trading-stock-thailand/datasets/web_set_income.py
# sk 2018-12-24
# Objective to retrieve statistical data from yahoo finance page
# Sample from PTT.BK as a Ticker
# https://finance.yahoo.com/quote/BEAUTY.BK/key-statistics?p=BEAUTY.BK
# Method 1. getTableData, 2. createDataFrame, 3. writeCSVFile
#           4. writeCSVFile, 5. removeOldFile
###################################################################

import urllib2
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from os.path import join, exists
from os import  remove, makedirs
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

DIR_SEC_CSV = "../data/statistics"

def getTableData(symbol):

    url_string = "https://finance.yahoo.com/quote/"
    url_string += symbol
    url_string += "/key-statistics?p="
    url_string += symbol

    response = urllib2.urlopen(url_string)
    page = response.read()
    soup = BeautifulSoup(page,'lxml')

    table_element = soup.findAll('table',class_="table-qsp-stats Mt(10px)")

    return table_element

def createDataFrame(table_element):
    #Generate lists
    row_list =[]
    index_list = []

    if table_element is None:
        return None

    num_col = 2
    count = 0

    for i in table_element:
        for row in i.findAll("td"):
            txt = row.find(text=True)
            count = count + 1
            if count % num_col == 1:
                index_list.append(txt)
            else:
                row_list.append(txt)

    # skip 'Statement of Comprehensive Income (MB.) and 'more'
    # index_list = index_list[1:len(index_list)-1]

    # skip first row :sk
    # index_list = index_list[1:len(index_list)]

    # num_col_df = num_col-1
    # shape_row = len(row_list)/num_col_df
    # row_list = np.reshape(row_list, (shape_row,num_col_df))
    #
    # all_head = row_list[0]
    # all_row = row_list[1:]
    # df = pd.DataFrame(columns = all_head, index = index_list, data = all_row)
    df = pd.DataFrame(columns=None,index = index_list, data = row_list)
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

    # symbol_list = ['PTT.BK','BEAUTY.BK', 'IRPC.BK', 'SPA.BK','TNH.BK','SCC.BK',
    #                'SPALI.BK','SPCG.BK','EA.BK']
    # typ = ['BS','IS','CF']
    #
    # for symbol in symbol_list:
    #     for finTyp in typ:
    symbol = 'PTT.BK'
    table_element = []
    table_element = getTableData(symbol)
    df = createDataFrame(table_element)
    print(df)
            # removeOldFile(symbol, finTyp) # clear old
            # writeCSVFile(df, symbol, finTyp, include_index = True)
