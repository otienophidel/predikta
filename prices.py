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
       
    def get_historical_prices(self):
         # NSE API endpoint for user specified company
        url = f"https://www.nse.co.ke/api/price-list?company={self.company_symbol}"

        # start date for prices = today
        start_date = datetime.datetime.today()
        start_date_str = start_date.strftime('%Y-%m-%d')

        # Set end date == 3000 days ago
        end_date = datetime.datetime.today() - datetime.timedelta(days=3000)
        end_date_str = end_date.strftime("%Y-%m-%d")

        # Adding start and end date to query parameters
        params = {
            "startDate": start_date_str,
            "endDate": end_date_str
        }

        # Sending HTTP request to api endpoint - with params
        response = requests.get(url, params=params, verify=False)

        if response.content:
            # Parse json response
            data = json.loads(response.content)
        else:
            print("Check response")
        
        # Extract historical stock prices from response
        prices = data['data']

        # Write historical prices to a .csv file
        filename = f"{self.company_symbol}_stock_prices.csv"
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Close_Price', 'High', 'Low', 'Average', 'Previous Day'])

            for i, price in enumerate(prices):
                if i == 0:
                    previous_day_close = ''
                else:
                    previous_day_close = prices[i-1]['Close']
                date = price['Date']
                close_price = price['Close']
                high = price['High']
                low = price['Low']
                average = price['Average']
                writer.writerow([date, close_price, high, low, average, previous_day_close])
        
        # Print confirmation message
        print(f"Historical {self.company_symbol} prices have been saved to {filename}")

def main():
    if len(sys.argv) != 2:
        print("Missing arguments")
        print("Usage: python {sys.argv[0]} SYMBOL")
        print("Example: python {sys.argv[0]} SCOM")
        sys.exit
    
    # Get company symbol fromargs
    company_symbol = sys.argv[1]
    print("Downloading historical stock prices for {sys.argv[1]}")
    stock_prices = StockPrices(company_symbol)
    stock_prices.get_historical_prices()

if __name__ == "__main__":
    main()