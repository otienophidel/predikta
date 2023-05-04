"""
# A file to download historical stock market prices
# Usage:
#		>>> python prices.py <SYMBOL>
#		Arguments:
#			SYMBOL - Company's stock market symbol
#
"""

import requests
import json
import csv
import datetime
import sys

# A class to communicate with NSE api endpoint
class StockPrices:
    def __init__(self, company_symbol):
        self.company_symbol = company_symbol
       
    def get_historical prices(self):
         # NSE API endpoint for user specified company
        url = f"https://www.nse.co.ke/api/price-list?company={self.company_symbol}"

        # start date for prices = today
        start_date = datetime.datetime.now()
        start_date = start_date.strftime('%Y-%m-%d')
    