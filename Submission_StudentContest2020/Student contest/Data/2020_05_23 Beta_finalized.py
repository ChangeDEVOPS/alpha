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
# https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?serietype=line
# https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?from=2018-03-12&to=2019-03-12


from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
from datetime import date
import datetime
import pandas as pd
import requests
import numpy as np
from math import *

# final_list = ['MSFT', 'AAPL', 'AMZN', 'GOOG', 'FB', 'INTC']
final_name = ['Microsoft', 'Apple', 'Amazon', 'Alphabet', 'Facebook']
final_list = ['MSFT', 'AAPL', 'AMZN', 'GOOG', 'FB']
final_list2 =  final_list

# assert len(final_list2) == 5

budget_dict = {}
n_stockdict = {}
n_stockslist = []

API_Key = "1739a7079e2840f6f77b92aa131e169e"

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

print("Do you want to buy an equal n. of shares for each stock in the portfolio?")
portfolio_distribution = input(
    "'https://www.investopedia.com/terms/p/portfolio.asp'(e.g equally-distributed portfolio)[y/n]: ").upper()

if portfolio_distribution == "Y":
    n_shares = int(input('How many equal n. of shares you want to invest in each stock? (e.g 100): '))
    for i in final_list2:
        budget_dict[i] = n_shares
    print()
    print("Here is the choosen portfolio distribution:")
    print(budget_dict)
    print()

elif portfolio_distribution == "N":

    for i in range(len(final_list2)):
        n_stocks = input("How many shares do you want to invest in '"+final_list2[i]+"' - "+final_name[i]+" (e.g 100)?: ")
        n_stockdict[final_list2[i]] = n_stocks
        n_stockslist.append(n_stocks)

    print()
    print("Here is the choosen portfolio distribution:")
    print(n_stockdict)
    print()

print("Are you well aware of the inherent risks involved in stock market investing, your risk profile and strategy?")
disclaimer = input("'https://www.investopedia.com/terms/r/risk.asp'\n\
'https://www.investopedia.com/terms/r/risk-profile.asp'\n\
'https://www.investopedia.com/terms/a/assetallocation.asp'[y/n]: ").upper()
if disclaimer == "Y":
    print()
elif disclaimer == "N":
    print()
    print("... carefully read the documentation before proceeding!")
    print("Stock investing can result in significant loss of your invested capital.")
    print("We therefore deny all resposibilities for actions or deeds deriving from the use of this software. CHANGE INVESTMENTS Ltd.")
    print()
else:
    print("Invalid input!")
    print()


current_date = str(date.today())
initial_time_period = input("Enter starting time period of performance (end=current date,default)(e.g 2020-01-01): ")
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
    performance = round((endprice / initialprice - 1)*100, 2)
    performance_list.append(performance)
    # calculate market capitalization
    if portfolio_distribution == "Y":
        initial_n_stock[i] =  budget_dict[i] 
        # print(initial_n_stock[i])
        i_stockcapitalization[i] = round(initial_n_stock[i] * initialprice, 2)
        e_stockcapitalization[i] = round(initial_n_stock[i] * endprice, 2)
        a = (100/len(final_list2)) * (e_stockcapitalization[i] / i_stockcapitalization[i])
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
index_query_value = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/index/%5EGSPC?from={initial_time_period}&to={end_time_period}&apikey={API_Key}').json()

# print(index_query_value)

sp500_initialprice = round(index_query_value['historical'][-1]['adjClose'],2)
sp500_endprice = round(index_query_value['historical'][0]['adjClose'],2)
sp500_performance = (sp500_endprice / sp500_initialprice - 1)*100


performance_list2 = []
for i in performance_list:
  performance_list2.append(i)
performance_list2.append(round(sp500_performance,2))
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
                    index= final_list2)
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
df2 = pd.DataFrame({'Performance(%)': [round(portfolio_perf,2), round(sp500_performance, 2), round(alpha_value, 2)]},
                    index=['Selected portfolio', 'S&P500', 'Result (Selected portfolio - S&P500)' ])
print(df2)
print()
print("**********************************************************************")
print("**********************************************************************")
print("Your selected portfolio's strategy VS S&P500 performance over the time period was\n\
'https://www.investopedia.com/terms/a/alpha.asp': >>>", color.BOLD, color.RED, round(alpha_value, 2), color.END, "% <<<")

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
#SP500 price
sp500_closes = []
for i in reversed(index_query_value['historical']):
    adjClose = round(i['adjClose'],2)
    sp500_closes.append(adjClose)
# print(sp500_closes)

#poltfolio price
portfolios_closes = {}
# print(final_list)
# print(final_list2)
for i in final_list:
    query_value = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{i}?from={initial_time_period}&to={end_time_period}&apikey={API_Key}').json()
    # print(query_value)
    try:
        for v in reversed(query_value['historical']):
            key = v['date']
            value = v['adjClose']
            portfolios_closes.setdefault(key,[]).append(value)
    except:
        continue

# print(portfolios_closes)
#Calculates final portfolio price according to portfolio_distribution(Y or N)
portfolios_pricelist = []
portfolios_pricelist2 = []
portfolios_adjusted_pricelist = []

if portfolio_distribution == "Y":
    for x,y in portfolios_closes.items():
        portfolios_pricelist.append(y)
elif portfolio_distribution == "N":
    for x,y in portfolios_closes.items():
        portfolios_pricelist.append(y)
# print(portfolios_pricelist)

if portfolio_distribution == "Y":
    # print(len(portfolios_pricelist))
    # print(portfolios_pricelist)
    for i in range(len(portfolios_pricelist)):
        a_list = []
        for j in range(len(portfolios_pricelist[i])):
            a = portfolios_pricelist[i][j] / portfolios_pricelist[0][j] *(100/len(final_list2))
            a_list.append(a)
        l = sum(a_list)
        portfolios_pricelist2.append(l)

elif portfolio_distribution == "N":
    for i in range(len(portfolios_pricelist)):
        a_list = []
        f_list = []
        for j in range(len(portfolios_pricelist[i])):
            a = portfolios_pricelist[i][j] *int(n_stockslist[j])
            f = portfolios_pricelist[0][j] *int(n_stockslist[j])
            a_list.append(a)
            f_list.append(f)

        l = 100 *((sum(a_list))/(sum(f_list)))
        portfolios_pricelist2.append(l)
# print(portfolios_pricelist2)

for i in range(len(portfolios_pricelist2)):
    a = portfolios_pricelist2[i] / portfolios_pricelist2[0]
    adjusted_price = round((a * sp500_closes[0]),2)
    portfolios_adjusted_pricelist.append(adjusted_price)
# print(portfolios_adjusted_pricelist)

#Set date
dates = []
for i in reversed(index_query_value['historical']):
    d = (i['date'])
    dates.append(d)
# print(dates)

#Display Graph
plt.plot(dates, sp500_closes, label = 'S&P500')
plt.plot(dates, portfolios_adjusted_pricelist, label = 'Portfolio')
plt.xticks(dates[::7], rotation=45, size='small')
plt.title('Portfolio vs S&P500', fontsize = 20)
plt.gcf().canvas.set_window_title('Performance comparison')
plt.grid(True)
plt.legend(loc = 'lower left', fontsize = 15)
plt.show()
