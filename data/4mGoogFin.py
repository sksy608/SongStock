#############################################################################################
# 4mGoogFin.py
# Download Data from Google Finance
# DErived from https://www.patanasongsivilai.com/blog/
#  stock-thai-python/?fbclid=IwAR3t4rMoPcSHlon5NNqLdLFYEM5xvvtfF7igHZ3PRSt2PbtMkXtkxo4n4kg
# Create on 2018-11-11
##############################################################################################

from googlefinance import getQuotes
import json, sys
try:
    symbol = 'AAPL'
    print(json.dumps(getQuotes(symbol), indent=2))
    print()
except:
    print("Error:", sys.exc_info()[0])
    print("Description:", sys.exc_info()[1])
