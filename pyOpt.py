"""
Author: T.T. Ouzounellis Kavlakonis
Description: Markowitz Efficient Frontier Portfolio Optimization 
using Python
"""

# import needed modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import datetime as dt  
import sys 
import os
from dateutil.relativedelta import relativedelta

#Function to show progress bar
def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i - %.1f%%\r" % (prefix, "#"*x, "."*(size-x), j, count, 100*j/count))
        file.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\nDone\n")
    file.flush()

#function to save data locally
def get_data_from_yahoo(tickers, startDate, endDate):
    # Create a path to save all the stock data as .csv files
    if not os.path.exists('./stock_dfs'):
        os.makedirs('./stock_dfs')

    # save data for the listed companies
    for ticker in progressbar(tickers, "Downloading Data: "):
        #if the file does not exist create it
        if not os.path.exists('./stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', startDate, endDate)
            df.to_csv('./stock_dfs/{}.csv'.format(ticker))
        #if the file exists update it
        else:
            os.remove('./stock_dfs/{}.csv'.format(ticker))
            df = web.DataReader(ticker, 'yahoo', startDate, endDate)
            df.to_csv('./stock_dfs/{}.csv'.format(ticker))


#function to compile data in usable form
def compile_data(tickers):
    main_df = pd.DataFrame()
    for ticker in tickers:
        df = pd.read_csv('./stock_dfs/{}.csv'.format(ticker))
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)
        df['Ticker']=ticker
        main_df = pd.concat([main_df, df])

    main_df = main_df.reset_index()
    main_df.drop(['index'], 1, inplace=True)
    
    return main_df


#select tickers that comprise our portfolio investment
portfolioTickers = ['TSLA', 'F', 'BAC', 'GE', 'GOOGL']

#select start and end dates for our data 
#period relative to today
endDate = dt.datetime.now().strftime("%Y-%m-%d")
startDate = (dt.datetime.now() + relativedelta(years=-5)).strftime("%Y-%m-%d")

#custom period
# endDate = '2016-12-31'
# startDate = '2014-1-1'

# columns of tickers and their corresponding adjusted prices
get_data_from_yahoo(portfolioTickers, startDate, endDate)
data = compile_data(portfolioTickers)
clean = data.set_index('Date')
table = clean.pivot(columns='Ticker')

# calculate daily and annual returns of the stocks
returns_daily = table.pct_change()
returns_annual = returns_daily.mean() * 250

# get daily and covariance of returns of the stock
cov_daily = returns_daily.cov()
cov_annual = cov_daily * 250

# empty lists to store returns, volatility and weights of imiginary portfolios
port_returns = []
port_volatility = []
sharpe_ratio = []
stock_weights = []

# set the number of combinations for imaginary portfolios
num_assets = len(portfolioTickers)
num_portfolios = 50000

# populate the empty lists with each portfolios returns,risk and weights
for single_portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    returns = np.dot(weights, returns_annual)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
    sharpe = returns / volatility
    sharpe_ratio.append(sharpe)
    port_returns.append(returns)
    port_volatility.append(volatility)
    stock_weights.append(weights)

# a dictionary for Returns and Risk values of each portfolio
portfolio = {'Returns': port_returns,
             'Volatility': port_volatility,
             'Sharpe Ratio': sharpe_ratio}

# extend original dictionary to accomodate each ticker and weight in the portfolio
for counter,symbol in enumerate(portfolioTickers):
    portfolio[symbol+' Weight'] = [Weight[counter] for Weight in stock_weights]

# make a nice dataframe of the extended dictionary
df = pd.DataFrame(portfolio)

# get better labels for desired arrangement of columns
column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' Weight' for stock in portfolioTickers]

# reorder dataframe columns
df = df[column_order]

# find min Volatility & max sharpe values in the dataframe (df)
min_volatility = df['Volatility'].min()
max_sharpe = df['Sharpe Ratio'].max()

# use the min, max values to locate and create the two special portfolios
sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
min_variance_port = df.loc[df['Volatility'] == min_volatility]

#plot frontier, max sharpe & min Volatility values with a scatterplot
plt.style.use('seaborn-dark')
df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='red', marker='D', s=200)
plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='blue', marker='D', s=200 )
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')

#print portfolios of interest and show the plot
print(sharpe_portfolio)
print(min_variance_port)
plt.show()


