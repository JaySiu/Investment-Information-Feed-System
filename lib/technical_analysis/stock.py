import os
import time
import talib
import datetime
import numpy as np
import pandas as pd
import module_path as mp
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import fix_yahoo_finance as yf

SLEEP_TIME = 1

def check_ticker_by_country(country):
    ticker_df = pd.read_csv(mp.dir_ta + 'Yahoo_Ticker_Symbols_Sep2017.csv')
    ticker_df = ticker_df[ticker_df.Country == country].sort_values(by='Ticker')
    ticker_dict_country = dict(zip(ticker_df.Ticker, ticker_df.Name))
    keys = list(ticker_dict_country.keys())
    keys.sort()
    for k in keys:
        print(k, ticker_dict_country[k])            # $chcp 65001 may be needed

def check_all_ticker(ticker):
    ticker_df = pd.read_csv(mp.dir_ta + 'Yahoo_Ticker_Symbols_Sep2017.csv')
    ticker_dict = dict(zip(ticker_df.Ticker, ticker_df.Name))
    return ticker_dict[ticker]

def check_stock_data_exist(ticker):
    if os.path.exists('data/{}.csv'.format(ticker)):
        os.remove('data/{}.csv'.format(ticker))
        return True
    else:
        return False

def stock_preprocess(ticker):
    print("Fetching {}'s data...".format(check_all_ticker(ticker)))
    end = datetime.datetime.today()
    start = end - datetime.timedelta(weeks=104)
    stock_df = yf.download(ticker, start=start, end=end)    # DataFrame
    if check_stock_data_exist(ticker):
        print("Has old data: %s" % True)
    else:
        print("Has old data: %s" % False)
    stock_df.to_csv(mp.dir_data + ticker + '.csv', index=False, encoding='utf_8_sig')
    time.sleep(SLEEP_TIME*3)
    print("***Stock data saved/updated***")
    stock_Close = np.array(stock_df.Close, dtype='f8')
    stock_Date = np.array(stock_df.index)
    stock_Date = np.array([datetime.datetime.strptime(str(t)[:10], '%Y-%m-%d').date() for t in stock_Date])

    return [stock_Date, stock_Close]
