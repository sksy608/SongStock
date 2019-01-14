#
# DL_FS.py
# http://market.sec.or.th/public/idisc/en/FinancialReport/FS-0000000564
# Land and House
# Objective:
#  1. Input Company Id to
#      http://market.sec.or.th/public/idisc/en/Viewmore/
#       fs-norm?uniqueIDReference=0000000564
#  2. Create list of links to Download.
#  3. Download from links.
# sk 2019-01-04
#
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests, zipfile, StringIO
import os


DIR_DATA = '../data/financials/'

def getTableData(CompanyId):

    url_string = 'http://market.sec.or.th/public/idisc/en/Viewmore/'
    url_string += 'fs-norm?uniqueIDReference='
    url_string += CompanyId

    response = urllib2.urlopen(url_string)
    page = response.read()
    soup = BeautifulSoup(page,'lxml')
    table_element = soup.findAll('table',
                                   class_='table table-striped table-hover')

    return table_element[len(table_element)-1]

def createDataFrame(table_element):

    if table_element is None:
        return None

    # columns list is yy-mm
    # row lists is a

    # create list
    row_list = []
    col_list = []

    num_col = 7
    count = 0
    i = 0
    ctxt = ''

    for row in table_element.findAll('td'):
        txt = row.find(text=True)
        count += 1
        i = count % num_col

        if i == 0:
            txt = row.a['href']
            row_list.append(txt)
        elif i == 2:
            ctxt += txt + '-'
        elif i == 5:
            ctxt += txt
            col_list.append(ctxt)
            ctxt = ''
        else:
            pass

    col_head = ['pos']

    df = pd.DataFrame(columns = col_head, index = col_list, data = row_list)
    return df

def downloadFile(df,symbol):
    # Download file
    for i in range(len(df)-1):
        f = df.iloc[i].pos
        if f.endswith('.zip'):
            r = requests.get(f, stream=True)
            z = zipfile.ZipFile(StringIO.StringIO(r.content))
            z.extractall()
            fs = ['AUDITOR_REPORT.DOC','NOTES.DOC',\
                    'FINANCIAL_STATEMENTS.XLSX','FINANCIAL_STATEMENTS.XLS']
            f_exist = [fe for fe in fs if os.path.exists(fe)]
            if f_exist:
                os.rename('AUDITOR_REPORT.DOC',\
                        DIR_DATA + df.iloc[i].name + '-' + symbol + '-AN.DOC')
                os.rename('NOTES.DOC',\
                        DIR_DATA + df.iloc[i].name + '-' + symbol + '-N.DOC')
                if os.path.exists('FINANCIAL_STATEMENTS.XLSX'):
                    os.rename('FINANCIAL_STATEMENTS.XLSX',\
                                DIR_DATA + df.iloc[i].name + '-' + symbol + \
                                '-FS.XLSX')
                else:
                    os.rename('FINANCIAL_STATEMENTS.XLS',\
                                DIR_DATA + df.iloc[i].name + '-' + symbol + \
                                '-FS.XLS')
            else:
                for fn in os.listdir('.'):
                    if fn.endswith('.doc')| \
                        fn.endswith('DOC')| \
                        fn.endswith('.xls'):
                        os.remove(fn)

if __name__ == '__main__':

    symbol_list = ['0000005001','0000001370']
    for symbol in symbol_list:
        table_element = getTableData(symbol)
        df = createDataFrame(table_element)
        downloadFile(df,symbol)
