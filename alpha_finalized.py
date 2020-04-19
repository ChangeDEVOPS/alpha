# # API SOURCES
# https://financialmodelingprep.com/developer/docs/
# https://fmpcloud.io/api
# https://www.multpl.com/sitemap
# https://fmpcloud.io/api/v3/ratios/AAPL?apikey=08fb3433c1c9a1930ea04b4ef285c321
# https://fmpcloud.io/api/v3/stock-screener?sector=tech&betaMoreThan=1.2&marketCapLowerThan=10000000000&limit=100&apikey=08fb3433c1c9a1930ea04b4ef285c321
# #

import requests


sector = input("Enter market of choice (e.g tech): ")  # {sector}
beta_l = input("Enter minimum beta 'https://www.investopedia.com/terms/b/beta.asp' (e.g 0): ")  # {beta_l}
beta_m = input("Enter maximum beta 'https://www.investopedia.com/terms/b/beta.asp' (e.g 3): ")  # {beta_m}
capitalization_l = int(
    input("Enter minimum stock capitalization in billion dollars (e.g 500): ")) * 1000000000  # {capitalization_l}
capitalization_m = int(
    input("Enter maximum stock capitalization in billion dollars (e.g 3000): ")) * 1000000000  # {capitalization_h}
number_stocks = input("Enter maximum number of stocks in the portfolio (e.g 10): ")  # {number_stocks}

API_key = "08fb3433c1c9a1930ea04b4ef285c321"

query_data = requests.get \
    ((f'https://fmpcloud.io/api/v3/stock-screener?sector={sector}&betaMoreThan={beta_l}&betaLessThan={beta_m}\
    &marketCapMoreThan={capitalization_l}&marketCapLessThan={capitalization_m}&limit={number_stocks}&apikey={API_key}'))

query_data = query_data.json() # convert to readable format

print()
print("Preliminary portfolio has", len(query_data), "stocks.")
print()

for item in query_data:
    print("Ticker:", item['symbol'], "-", item['companyName'])




while True:
    print()
    stock_ticker = input\
        ("Enter stock ticker (e.g AAPL) to investigate key ratios or 'done' to quit: ").upper()  # {stock_ticker}
    if stock_ticker == "DONE":
        break

    query_ratios = requests.get\
        ((f'https://fmpcloud.io/api/v3/ratios/{stock_ticker}?apikey={API_key}'))
    query_ratios = query_ratios.json()
    current_year_ratios = query_ratios[0].items()
    print()

    pos = 0
    for k in current_year_ratios:
        print(pos, k)
        # print(pos,"Key metric: ", k[0],"-",k[1]) ---nice output
        pos += 1

final_portfolio = []
print()

max_priceEarningsRatio= float(input\
    ("Enter maximum value for PE Ratio\n\
    https://www.investopedia.com/terms/p/price-earningsratio.asp (e.g 100) (min == 0,default): "))
max_priceToBookRatio = float(input\
    ("Enter maximum value for PB Ratio \n\
    https://www.investopedia.com/terms/p/price-to-bookratio.asp (e.g 100) (min == 0,default): "))
min_returnOnEquity = float(input\
    ("Enter minimum value for ROE\n\
    https://www.investopedia.com/terms/r/returnonequity.asp (e.g 0.01) (min == 0,default): "))
min_netProfitMargin = float(input\
    ("Enter minimum value for Profit Margin\n\
    https://www.investopedia.com/terms/p/profitmargin.asp (e.g 0.01) (min == 0,default): "))
print()

for item in query_data:
    stock_ticker = item['symbol']
    try:
        query_ratios = requests.get\
            ((f'https://fmpcloud.io/api/v3/ratios/{stock_ticker}?apikey={API_key}'\
              .format(stock_ticker=stock_ticker, API_key=API_key))) # HERE I HAVE ISSUE THE QUERY DOESN'T WORK FOR ALL TICKER - JUST "FB"
        query_ratios = query_ratios.json()
    #print(query_ratios)
        current_year_ratios = query_ratios[0].items()
    # print()
    # print(current_year_ratios)


        PB = None
        ROE = None
        PM = None
        PE = None

        for (k, v) in current_year_ratios:
            if k == "priceEarningsRatio":
                PE = float(v)
            if k == "priceToBookRatio":
                PB = float(v)
            if k == "returnOnEquity":
                ROE = float(v)
            if k == "netProfitMargin":
                PM = float(v)

        if PE < max_priceEarningsRatio\
                and PB < max_priceToBookRatio\
                and ROE > min_returnOnEquity\
                and PM > min_netProfitMargin:

            final_portfolio.append(item)
            print("Ticker:", item['symbol'], "-", item['companyName']," has PE of", round(PE,4))
            print("Ticker:", item['symbol'], "-", item['companyName']," has PB of", round(PB,4))
            print("Ticker:", item['symbol'], "-", item['companyName']," has ROE of", round(ROE,4))
            print("Ticker:", item['symbol'], "-", item['companyName']," has PM of", round(PM,4))
            print()
    except:
        pass

print()
print("Finalized portfolio has", len(final_portfolio), "stocks.")
print()

for item in final_portfolio:
    print("Ticker:", item['symbol'], "-", item['companyName'])



# except:
#     print("... your input are not in range! Try again.")

# name_stock_s = {}
# for i in name_stock_l:
#     set.add(name_stock_s,i)
#
# print(name_stock_s)

# for stock in tickers:
#     priceEarningsRatio = getPtE(stock)
#     if 0 <= priceEarningsRatio <= 10:
#         portfolio.append(PEratio)
#         print("The P/E ratio of ticker", tickers[tickers.index(stock)], \
#               name_stock[tickers.index(stock)], "is: ", PEratio)
