# # API SOURCES
# https://financialmodelingprep.com/developer/docs/
# https://fmpcloud.io/
# https://www.multpl.com/sitemap
# https://www.quandl.com/data/MULTPL-S-P-500-Ratios
# https://fmpcloud.io/api/v3/ratios/AAPL?apikey=08fb3433c1c9a1930ea04b4ef285c321
# https://fmpcloud.io/api/v3/stock-screener?sector=tech&betaMoreThan=1.2&marketCapLowerThan=10000000000&limit=100&apikey=08fb3433c1c9a1930ea04b4ef285c321

# #while True:
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
from datetime import date
import datetime
import pandas as pd
import requests
import numpy as np
from math import *
import requests

# API_KEY SECTION: WE ONLY USED OPEN SOURCE DATA AVAILABLE WITH FREE SUBSCRIPTION PLANS
API_key0 = "696yQxZ1z--8iu9XLzCP" #https://www.quandl.com
API_key = "d7b0cea15ad8d7758a881cd894153bd4" #https://fmpcloud.io
API_Key = "8382faee62cfb02aa4dfbcff95d50a4c" #https://financialmodelingprep.com/

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

print("Project Description – ALPHA (α)")
print()
print("The software will be deployed to calculate average PE Ratio [1] and other relevant measures of a market index of choice (e.g. S&P500 [2]) \n and then compare it with PE and other ratios of each individual stock listed in the chosen market index composition. \n"\
"As starting point, by developing an alpha version of the software, the goal will be to select those stocks with relevant mispricing \n and whose ratios are undervalued relative to the current market benchmark.\n "\
"General purpose of the software version will be to propose an efficient and automatic portfolio selection (descriptive model),\n assuring to the user (client) measurable active return against the index, so called α [3].\n" \
"Later features, added by developing beta version, will be the capability of the software to automatically build a portfolio of stocks \n and measure his performance against historical events (diagnostic model – back test data). \n")
print("For more info, please read the project description...")
print()
print("Chosen index benchmark: >>> S&P 500 <<<")
print()
print("SP500_SHILLER_PE_RATIO_MONTH (Shiller PE): "+ str(query_data00['dataset']['data'][0][1]) + ' as of ' + str(query_data00['dataset']['data'][0][0]))
print("'https://www.investopedia.com/terms/c/cape-ratio.asp'")
print("SP500_PE_RATIO_MONTH (PE): " + str(query_data0['dataset']['data'][0][1]) + ' as of ' + str(query_data0['dataset']['data'][0][0]))
print("'https://www.investopedia.com/terms/p/price-earningsratio.asp'")
print("SP500_DIV_YIELD%_MONTH (ROE): " + str((query_data1['dataset']['data'][0][1])) + ' as of ' + str(query_data1['dataset']['data'][0][0]))
print("'https://www.investopedia.com/terms/d/dividendyield.asp'")
print("SP500_EARNINGS_YIELD%_MONTH (PM): " + str((query_data2['dataset']['data'][0][1])) + ' as of ' + str(query_data2['dataset']['data'][0][0]))
print("https://www.investopedia.com/terms/e/earningsyield.asp")
print()

try:
    sector = input("Enter market sector of choice (e.g tech, financial, energy) \n\
'https://www.investopedia.com/terms/s/sector-breakdown.asp': ").lower()  # {industry_sector}
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
    ####################################################################################################################
    ####################################################################################################################
    #BETA VERSION 2.0

    # API SOURCES:
    # https://financialmodelingprep.com/api/v3/symbol/available-indexes
    # https://financialmodelingprep.com/api/v3/historical-price-full/index/%5EGSPC
    # https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?serietype=line
    # https://financialmodelingprep.com/api/v3/company/profile/AAPL
    # https://financialmodelingprep.com/api/v3/quote/AAPL
    # https://financialmodelingprep.com/api/v3/financial-ratios/AAPL
    # https://financialmodelingprep.com/api/v3/enterprise-value/AAPL
    # https://financialmodelingprep.com/api/v3/enterprise-value/AAPL?period=quarter
    # https://financialmodelingprep.com/api/v3/company-key-metrics/AAPL
    # https://financialmodelingprep.com/api/v3/company-key-metrics/AAPL?period=quarter
    # https://financialmodelingprep.com/api/v3/historical-price-full/AAPL
    # https://financialmodelingprep.com/api/v3/historical-price-full/AAPL
    # https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?serietype=line
    # https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?from=2018-03-12&to=2019-03-12

    # final_list = ['MSFT', 'AAPL', 'AMZN', 'GOOG', 'FB', 'INTC']
    # final_name = ['Microsoft', 'Apple', 'Amazon', 'Alphabet', 'Facebook']
    # final_list = ['MSFT', 'AAPL', 'AMZN', 'GOOG', 'FB']
    final_list2 = final_list

    # assert len(final_list2) == 5

    equalnum_dict = {}
    n_stockdict = {}
    n_stockslist = []

    # while True:
    #     stock_ticker = input("Enter a ticker (e.g AAPL) in your portfolios (5 stocks) or just 'done' to move forward: ").upper()
    #     final_list.append(stock_ticker)
    #     final_list2.append(stock_ticker)
    #     if stock_ticker == "DONE":
    #         final_list.remove('DONE')
    #         final_list2.remove('DONE')
    #         if len(final_list) == 5:
    #             break
    #         else:
    #             print('You have to enter five stocks.')
    #             final_list.clear()
    #             final_list2.clear()
    #
    # print(final_list2)

    #  PROMPT : PORTFOLIO COMPOSITION ? EQUALLY DISTRIBUTED / DIFFERENT WEIGHT
    print()
    print("Do you want to buy an equal n. of shares for each stock in the portfolio?")
    portfolio_distribution = input(
        "'https://www.investopedia.com/terms/p/portfolio.asp'(e.g equally-distributed portfolio)[y/n]: ").upper()

    if portfolio_distribution == "Y":
        n_shares = int(input('How many equal n. of shares you want to invest in each stock? (e.g 100): '))
        for i in final_list2:
            equalnum_dict[i] = n_shares
        print()
        print("Here is the chosen portfolio distribution:")
        print(equalnum_dict)
        print()

    elif portfolio_distribution == "N":

        for i in range(len(final_list2)):
            n_stocks = input("How many shares do you want to invest in '" + final_list2[i] + "' - " + final_name[
                i] + " (e.g 100)?: ")
            n_stockdict[final_list2[i]] = n_stocks
            n_stockslist.append(n_stocks)

        print()
        print("Here is the chosen portfolio distribution:")
        print(n_stockdict)
        print()

    print(
        "Are you well aware of the inherent risks involved in stock market investing, your risk profile and strategy?")
    disclaimer = input("'https://www.investopedia.com/terms/r/risk.asp'\n\
    'https://www.investopedia.com/terms/r/risk-profile.asp'\n\
    'https://www.investopedia.com/terms/a/assetallocation.asp'[y/n]: ").upper()
    if disclaimer == "Y":
        print()
    elif disclaimer == "N":
        print()
        print("... carefully read the documentation before proceeding!")
        print("Stock investing can result in significant loss of your invested capital.")
        print(
            "We therefore deny all resposibilities for actions or deeds deriving from the use of this software. CHANGE INVESTMENTS Ltd.")
        print()
    else:
        print("Invalid input!")
        print()

    current_date = str(date.today())
    initial_time_period = input(
        "Enter starting time period of performance (end=current date,default)(e.g 2020-01-01): ")
    end_time_period = current_date

    initialprice_list = []
    endprice_list = []
    performance_list = []
    initial_n_stock = {}
    i_stockcapitalization = {}
    e_stockcapitalization = {}
    portfoliocapital = []
    im = []
    em = []
    for i in final_list2:
        query_value = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/\
        {i}?from={initial_time_period}&to={end_time_period}&apikey={API_Key}').json()
        # print(query_value)

        initialprice = query_value['historical'][-1]['adjClose']
        initialprice_list.append(initialprice)
        endprice = (query_value['historical'][0]['adjClose'])
        endprice_list.append(endprice)
        performance = round((endprice / initialprice - 1) * 100, 2)
        performance_list.append(performance)
        # calculate market capitalization
        if portfolio_distribution == "Y":
            initial_n_stock[i] = equalnum_dict[i]
            # print(initial_n_stock[i])
            i_stockcapitalization[i] = round(initial_n_stock[i] * initialprice, 2)
            e_stockcapitalization[i] = round(initial_n_stock[i] * endprice, 2)
            a = (100 / len(final_list2)) * (e_stockcapitalization[i] / i_stockcapitalization[i])
            portfoliocapital.append(a)
            # print(portfoliocapital)
            # b = sum(portfoliocapital)
            # print(b)
            # portfolio_perf = b / 100 - 1

        elif portfolio_distribution == "N":
            i_stockcapitalization[i] = round(int(n_stockdict[i]) * initialprice, 2)
            im.append(i_stockcapitalization[i])
            e_stockcapitalization[i] = round(int(n_stockdict[i]) * endprice, 2)
            em.append(e_stockcapitalization[i])
            # print(em)
            # mc = 100 * (sum(em)/sum(im))
            # portfolio_perf = mc /100 - 1

    if portfolio_distribution == "Y":
        b = sum(portfoliocapital)
        # print(b)
        portfolio_perf = b - 100

    elif portfolio_distribution == "N":
        mc = 100 * (sum(em) / sum(im))
        portfolio_perf = mc - 100

    # Market_index
    index_query_value = requests.get(
        f'https://financialmodelingprep.com/api/v3/historical-price-full/index/%5EGSPC?from={initial_time_period}&to={end_time_period}&apikey={API_Key}').json()

    # print(index_query_value)

    sp500_initialprice = round(index_query_value['historical'][-1]['adjClose'], 2)
    sp500_endprice = round(index_query_value['historical'][0]['adjClose'], 2)
    sp500_performance = (sp500_endprice / sp500_initialprice - 1) * 100

    performance_list2 = []
    for i in performance_list:
        performance_list2.append(i)
    performance_list2.append(round(sp500_performance, 2))
    # print(performance_list2)
    initialprice_list.append(sp500_initialprice)
    # print(initialprice_list)
    endprice_list.append(sp500_endprice)
    # print(endprice_list)
    final_list2.append('GSPC')
    # print(final_list2)
    df = pd.DataFrame({'Performance(%)': performance_list2,
                       'Initial price($)': initialprice_list,
                       'End price($)': endprice_list},
                      index=final_list2)
    print()
    print("**********************************************************************")
    print("**********************************************************************")

    print(df)

    print()
    print("**********************************************************************")
    print("**********************************************************************")


    class color:
        BLUE = '\033[94m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        END = '\033[0m'


    alpha_value = portfolio_perf - sp500_performance
    df2 = pd.DataFrame(
        {'Performance(%)': [round(portfolio_perf, 2), round(sp500_performance, 2), round(alpha_value, 2)]},
        index=['Selected portfolio', 'S&P500', 'Result (Selected portfolio - S&P500)'])
    print(df2)
    print()
    print("**********************************************************************")
    print("**********************************************************************")
    print("Your selected portfolio's strategy VS S&P500 performance over the time period was\n\
    'https://www.investopedia.com/terms/a/alpha.asp': >>>", color.BOLD, color.RED, round(alpha_value, 2), color.END,
          "% <<<")

    if alpha_value > 0:
        print()
        print("...Your strategy" + color.BOLD + color.BLUE + " OUTPERFORMED " + color.END + "the market benchmark!")
    elif alpha_value < 0:
        print()
        print("...Your strategy" + color.BOLD + color.RED + " UNDERPERFORMED " + color.END + "the market benchmark!")
    else:
        print()
        print(color.BOLD + "...Your strategy performed as the market benchmark!" + color.END)

    print()
    print("**********************************************************************")
    print("**********************************************************************")

    # DATA VISUALIZATION SECTION
    #
    # SP500 price
    sp500_closes = []
    for i in reversed(index_query_value['historical']):
        adjClose = round(i['adjClose'], 2)
        sp500_closes.append(adjClose)
    # print(sp500_closes)

    # poltfolio price
    portfolios_closes = {}
    # print(final_list)
    # print(final_list2)
    for i in final_list:
        query_value = requests.get(
            f'https://financialmodelingprep.com/api/v3/historical-price-full/{i}?from={initial_time_period}&to={end_time_period}&apikey={API_Key}').json()
        # print(query_value)
        try:
            for v in reversed(query_value['historical']):
                key = v['date']
                value = v['adjClose']
                portfolios_closes.setdefault(key, []).append(value)
        except:
            continue

    # print(portfolios_closes)
    # Calculates final portfolio price according to portfolio_distribution(Y or N)
    portfolios_pricelist = []
    portfolios_pricelist2 = []
    portfolios_adjusted_pricelist = []

    if portfolio_distribution == "Y":
        for x, y in portfolios_closes.items():
            portfolios_pricelist.append(y)
    elif portfolio_distribution == "N":
        for x, y in portfolios_closes.items():
            portfolios_pricelist.append(y)
    # print(portfolios_pricelist)

    if portfolio_distribution == "Y":
        # print(len(portfolios_pricelist))
        # print(portfolios_pricelist)
        for i in range(len(portfolios_pricelist)):
            a_list = []
            for j in range(len(portfolios_pricelist[i])):
                a = portfolios_pricelist[i][j] / portfolios_pricelist[0][j] * (100 / len(final_list2))
                a_list.append(a)
            l = sum(a_list)
            portfolios_pricelist2.append(l)

    elif portfolio_distribution == "N":
        for i in range(len(portfolios_pricelist)):
            a_list = []
            f_list = []
            for j in range(len(portfolios_pricelist[i])):
                a = portfolios_pricelist[i][j] * int(n_stockslist[j])
                f = portfolios_pricelist[0][j] * int(n_stockslist[j])
                a_list.append(a)
                f_list.append(f)

            l = 100 * ((sum(a_list)) / (sum(f_list)))
            portfolios_pricelist2.append(l)
    # print(portfolios_pricelist2)

    for i in range(len(portfolios_pricelist2)):
        a = portfolios_pricelist2[i] / portfolios_pricelist2[0]
        adjusted_price = round((a * sp500_closes[0]), 2)
        portfolios_adjusted_pricelist.append(adjusted_price)
    # print(portfolios_adjusted_pricelist)

    # Set date
    dates = []
    for i in reversed(index_query_value['historical']):
        d = (i['date'])
        dates.append(d)
    # print(dates)

    # Display Graph
    plt.plot(dates, sp500_closes, label='S&P500')
    plt.plot(dates, portfolios_adjusted_pricelist, label='Portfolio')
    plt.xticks(dates[::7], rotation=45, size='small')
    plt.title('Portfolio vs S&P500', fontsize=20)
    plt.gcf().canvas.set_window_title('Performance comparison')
    plt.grid(True)
    plt.legend(loc='lower left', fontsize=15)
    plt.show()



except:
    print()
    print("... your inputs are not valid! Try again.")
    print()


