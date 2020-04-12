import pandas as pd
import requests
stock = input("Enter stock ticker (e.g AAPL): ")
# market = input("Enter market of choice (e.g NASDAQ): ") #'+market+f'

PtE = {}
API_key = "08fb3433c1c9a1930ea04b4ef285c321"
query_data = requests.get\
((f'https://fmpcloud.io/api/v3/search?query=&exchange=NASDAQ&limit=5000&apikey={API_key}'))

query_data = query_data.json() # convert to readable format

list_500 = query_data

# for i in list_500:
#     print(i)

def getPtE (stock):

    income_statement= requests.get\
    (f"https://financialmodelingprep.com/api/v3/financials/income-statement/{stock}")
    income_statement = income_statement.json()
    earnings = float(income_statement['financials'][0]['Net Income'])
   # print(income_statement)

    company_info = requests.get\
    (f"https://financialmodelingprep.com/api/v3/company/profile/{stock}")
    company_info = company_info.json()
    market_cap = float(company_info['profile']['mktCap'])

    Price_to_Earnings = market_cap / earnings
    PtE[stock] = Price_to_Earnings
    return PtE

print("The P/E ratio of ticker",stock,"is: ", getPtE(stock))


