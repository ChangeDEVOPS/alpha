# # API SOURCES
# https://financialmodelingprep.com/developer/docs/
# https://fmpcloud.io/
# https://www.multpl.com/sitemap
# https://www.quandl.com/data/MULTPL-S-P-500-Ratios
# https://fmpcloud.io/api/v3/ratios/AAPL?apikey=08fb3433c1c9a1930ea04b4ef285c321
# https://fmpcloud.io/api/v3/stock-screener?sector=tech&betaMoreThan=1.2&marketCapLowerThan=10000000000&limit=100&apikey=08fb3433c1c9a1930ea04b4ef285c321

# #while True:
import requests

# S&P500 PER
API_key0 = "696yQxZ1z--8iu9XLzCP"


query_data00 = requests.get\
    ((f'https://www.quandl.com/api/v3/datasets/MULTPL/SHILLER_PE_RATIO_MONTH.json?api_key={API_key0}'))
query_data0 = requests.get\
    ((f'https://www.quandl.com/api/v3/datasets/MULTPL/SP500_PE_RATIO_MONTH.json?api_key={API_key0}'))
query_data1 = requests.get\
    ((f'https://www.quandl.com/api/v3/datasets/MULTPL/SP500_DIV_YIELD_MONTH.json?api_key={API_key0}'))
query_data2 = requests.get\
    ((f'https://www.quandl.com/api/v3/datasets/MULTPL/SP500_EARNINGS_YIELD_MONTH.json?api_key={API_key0}'))


query_data00 = query_data00.json()
query_data0 = query_data0.json()
query_data1 = query_data1.json()
query_data2 = query_data2.json()

print()
print("SHILLER_PE_RATIO_MONTH (Shiller PE): "+ str(query_data00['dataset']['data'][0][1]) + ' as of ' + str(query_data00['dataset']['data'][0][0]))
print()
print("SP500_PE_RATIO_MONTH (PE): " + str(query_data0['dataset']['data'][0][1]) + ' as of ' + str(query_data0['dataset']['data'][0][0]))
print("SP500_DIV_YIELD%_MONTH (ROE): " + str((query_data1['dataset']['data'][0][1])) + ' as of ' + str(query_data1['dataset']['data'][0][0]))
print("SP500_EARNINGS_YIELD%_MONTH (PM): " + str((query_data2['dataset']['data'][0][1])) + ' as of ' + str(query_data2['dataset']['data'][0][0]))
print()

try:
    sector = input("Enter market sector of choice (e.g tech, financial, energy) \n\
'https://www.investopedia.com/terms/s/sector-breakdown.asp': ")  # {industry_sector}
    print("Beta ratio: B<0 (Negative correlation with the market)")
    print("0<B<1 (Positive correlation - Lower than market volatility)")
    print("B>1 (Positive correlation - Greater than market volatility)")
    beta_l = input("Enter minimum beta 'https://www.investopedia.com/terms/b/beta.asp' (e.g 0): ")  # {beta_l}
    beta_m = input("Enter maximum beta 'https://www.investopedia.com/terms/b/beta.asp' (e.g 3): ")  # {beta_m}
    print("Market capitalization: 0-50 (small) 50-500 (medium) 500 -5000 (big)\n\
'https://www.investopedia.com/terms/m/marketcapitalization.asp'") #capitalization_$
    capitalization_l = int(
        input("Enter minimum stock market capitalization in billion dollars (e.g 200): ")) * 1000000000  # {capitalization_l}
    capitalization_m = int(
        input("Enter maximum stock market capitalization in billion dollars (e.g 2000): ")) * 1000000000  # {capitalization_h}
    number_stocks = input("Enter maximum number of stocks in the portfolio (e.g 10): ")  # {number_stocks}

    API_key = "d7b0cea15ad8d7758a881cd894153bd4"

    query_data = requests.get \
        ((f'https://fmpcloud.io/api/v3/stock-screener?sector={sector}&betaMoreThan={beta_l}&betaLessThan={beta_m}\
        &marketCapMoreThan={capitalization_l}&marketCapLessThan={capitalization_m}&limit={number_stocks}&apikey={API_key}'))

    query_data = query_data.json() # convert to readable format

    print()
    print("Preliminary portfolio has", len(query_data), "stocks.")
    print()

    for item in query_data:
        print("Ticker:", item['symbol'], "-", item['companyName'])

    # preliminary_list = []
    # preliminary_data = []
    # print()
    #
    # for item in query_data:
    #     if item['companyName'] not in preliminary_list:
    #         preliminary_list.append(item['companyName'])
    #         preliminary_data.append(item)
    #         print("Ticker:", item['symbol'], "-", item['companyName'])
    # print()
    # print("Preliminary portfolio has", len(preliminary_data), "stocks.")
    # print()
    # HERE I WANTED TO REMOVE DUPLICATES FOR SAME COMPANY NAME IN PRELIMINARY PORTFOLIO
    # BUT IT'S ACCEPTABLE SINCE DIFFERENT TICKERS COULD INDICATE DIFFERENT TYPE OF PRIVILEGED SHARES FOR SAME COMPANY
    # ACCEPTED - POSSIBLE TO REMOVE IF UNCOMMENTED


    while True:
        try:
            print()
            stock_ticker = input\
                ("Enter stock ticker (e.g AAPL) to investigate key ratios or just 'done' to move forward: ").upper()  # {stock_ticker}
            if stock_ticker == "DONE":
                break

            query_ratios = requests.get\
                ((f'https://fmpcloud.io/api/v3/ratios/{stock_ticker}?apikey={API_key}'))
            query_ratios = query_ratios.json()
            current_year_ratios = query_ratios[0].items()
            print()

            pos = 0
            for k in current_year_ratios:
                # print(pos, k)
                print(pos,"Key metric: ", k[0],"-",k[1]) #---nice output
                pos += 1
        except:
            print()
            print("... your inputs are not valid! Try again.")
            continue
    print()

    max_priceEarningsRatio= float(input(f"Enter maximum value for PE Ratio\n\
'https://www.investopedia.com/terms/p/price-earningsratio.asp' (e.g 30)\
(Avg. Market Index == {str(query_data0['dataset']['data'][0][1])}): "))

    max_priceToBookRatio = float(input\
        (f"Enter maximum value for PB Ratio \n\
'https://www.investopedia.com/terms/p/price-to-bookratio.asp'(e.g 30)\
(min == 0,default): "))

    min_returnOnEquity = float(input\
        (f"Enter minimum value for ROE\n\
'https://www.investopedia.com/terms/r/returnonequity.asp'(e.g 0.01)\
(Avg. Market Index == {(query_data1['dataset']['data'][0][1])/100}): "))


    min_netProfitMargin = float(input\
        (f"Enter minimum value for Profit Margin\n\
'https://www.investopedia.com/terms/p/profitmargin.asp'(e.g 0.01)\
(Avg. Market Index == {(query_data2['dataset']['data'][0][1])/100}): "))

    print()

    final_data = []
    final_list = []
    final_name = []

    for item in query_data:
        stock_ticker = item['symbol']
        try:
            query_ratios = requests.get\
                ((f'https://fmpcloud.io/api/v3/ratios/{stock_ticker}?apikey={API_key}'\
                  .format(stock_ticker=stock_ticker, API_key=API_key)))
            # HERE I HAVE ISSUE THE QUERY DOESN'T WORK FOR ALL TICKERS #FIXED WITH TRY/EXCEPT

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
                    # if item['companyName'] not in final_name: # HERE I WANTED TO REMOVE DUPLICATES FOR SAME COMPANY NAME - IMPLEMENTED
                    # BUT IT'S ACCEPTABLE SINCE DIFFERENT TICKERS COULD INDICATE DIFFERENT TYPE OF PRIVILEGED SHARES FOR SAME COMPANY # ACCEPTED

                    if item['companyName'] not in final_name:
                        final_data.append(item)
                        final_name.append(item['companyName'])
                        final_list.append(item['symbol'])
                        print("Ticker:", item['symbol'], "-", item['companyName']," has PE of", round(PE, 4))
                        print("Ticker:", item['symbol'], "-", item['companyName']," has PB of", round(PB, 4))
                        print("Ticker:", item['symbol'], "-", item['companyName']," has ROE of", round(ROE, 4))
                        print("Ticker:", item['symbol'], "-", item['companyName']," has PM of", round(PM, 4))
                        print()
        except:
            pass

    print("******************************************************")
    print("******************************************************")
    print()

    # print(final_data)
    # print(final_list)
    # print(final_name)
    # print()

    for item in final_data:
            print("Ticker:", item['symbol'], "-", item['companyName'])

    print()
    print("Finalized portfolio has", len(final_name), "stocks.")
    print()
    print(final_list)
    print(final_name)

    # HERE I WANTED TO REMOVE DUPLICATES FOR SAME COMPANY NAME IN FINAL PORTFOLIO - IMPLEMENTED
    # BUT IT'S ACCEPTABLE SINCE DIFFERENT TICKERS COULD INDICATE DIFFERENT TYPE OF PRIVILEGED SHARES FOR SAME COMPANY
    # ACCEPTED - POSSIBLE TO REMOVE IF UNCOMMENTED
    # print(final_data)

    # print("Preliminary portfolio has", len(final_list), "stocks.")
    # print()
    # for item in final_data:
    #     print("Ticker:", item['symbol'], "-", item['companyName'])

    # print(final_data)

    #break #POSSIBLE TO MAKE THE PROGRAM RUN AS A LOOP IF UNCOMMENTED


except:
    print()
    print("... your inputs are not valid! Try again.")
    print()


