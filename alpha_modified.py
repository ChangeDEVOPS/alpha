import pandas as pd
import requests
# market = input("Enter market of choice (e.g NASDAQ): ") #{market}

API_key = "08fb3433c1c9a1930ea04b4ef285c321"
query_data = requests.get \
    ((f'https://fmpcloud.io/api/v3/search?query=&exchange=NASDAQ&limit=5000&apikey={API_key}'))

query_data = query_data.json()  # convert to readable format
#print(query_data)


tickers = []
name_stock = []
portfolio = []

for d in query_data:
    tickers.append(d['symbol'])
    name_stock.append(d['name'])
    if len(tickers) == 50:
        break

# print(ticker)
# print(name_stock)

def getPtE(stock):
    try:
        income_statement = requests.get \
            (f"https://financialmodelingprep.com/api/v3/financials/income-statement/{stock}")
        income_statement = income_statement.json()
        earnings = float(income_statement['financials'][0]['Net Income'])
        # print(income_statement)

        company_info = requests.get \
            (f"https://financialmodelingprep.com/api/v3/company/profile/{stock}")
        company_info = company_info.json()
        market_cap = float(company_info['profile']['mktCap'])

        Price_to_Earnings = market_cap / earnings
    except:
        Price_to_Earnings = -1000000
    return Price_to_Earnings


for stock in tickers:
    PEratio = getPtE(stock)
    if 0 <= PEratio <= 10:
        portfolio.append(PEratio)
        print("The P/E ratio of ticker", tickers[tickers.index(stock)], \
              name_stock[tickers.index(stock)], "is: ", PEratio)