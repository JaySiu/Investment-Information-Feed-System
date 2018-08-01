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
from matplotlib.finance import date2num

SLEEP_TIME = 1

'''
take a string of ticker
fetch the ticker's data from yahoo APIs
save the pandas Dataframe data as .to_csv
return a copy of the DataFrame with added 'Date' column
'''
def fetch_yahoo_data(ticker):
    print("Fetching {}'s data...".format(check_all_ticker(ticker)))
    end = datetime.datetime.today()
    start = end - datetime.timedelta(weeks=78)
    stock_df = yf.download(ticker, start=start, end=end)    # return a DataFrame
    time.sleep(SLEEP_TIME*2)
    if check_stock_data_exist(ticker):
        print("Has old data: %s" % True)
    else:
        print("Has old data: %s" % False)
    stock_df_cvs = stock_df
    stock_Date = np.array(stock_df.index)
    stock_df_cvs['Date'] = np.array([datetime.datetime.strptime(str(t)[:10], '%Y-%m-%d').date() for t in stock_Date])
    stock_df_cvs = stock_df_cvs[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
    stock_df_cvs.to_csv(mp.dir_data + ticker + '.csv', index=False, encoding='utf_8_sig')
    time.sleep(SLEEP_TIME*3)
    print("***Stock data saved/updated***")
    return stock_df


'''
take a string of country
print out the country's ticker-name mapping
'''
def check_ticker_by_country(country):
    ticker_df = pd.read_csv(mp.dir_ta + 'Yahoo_Ticker_Symbols_Sep2017.csv')
    ticker_df = ticker_df[ticker_df.Country == country].sort_values(by='Ticker')
    ticker_dict_country = dict(zip(ticker_df.Ticker, ticker_df.Name))
    keys = list(ticker_dict_country.keys())
    keys.sort()
    for k in keys:
        print(k, ticker_dict_country[k])            # $chcp 65001 may be needed


'''
take a string of ticker
return the name of the ticker
'''
def check_all_ticker(ticker):
    ticker_df = pd.read_csv(mp.dir_ta + 'Yahoo_Ticker_Symbols_Sep2017.csv')
    ticker_dict = dict(zip(ticker_df.Ticker, ticker_df.Name))
    return ticker_dict[ticker]


'''
take a string of ticker
check if the ticker's .csv file already exists
if exists, remove the file
'''
def check_stock_data_exist(ticker):
    if os.path.exists('data/{}.csv'.format(ticker)):
        os.remove('data/{}.csv'.format(ticker))
        return True
    else:
        return False


'''
take a string of ticker
return a list of the ticker's data coulmns as numpy arrays
-> for plotting normal curve
'''
def stock_preprocess_arr_list(ticker):
    stock_df = fetch_yahoo_data(ticker)
    stock_Open = np.array(stock_df.Open, dtype='f8')
    stock_High = np.array(stock_df.High, dtype='f8')
    stock_Low = np.array(stock_df.Low, dtype='f8')
    stock_Close = np.array(stock_df.Close, dtype='f8')
    stock_Volume = np.array(stock_df.Volume)
    stock_Date = np.array(stock_df.index)
    stock_Date = np.array([datetime.datetime.strptime(str(t)[:10], '%Y-%m-%d').date() for t in stock_Date])

    return [stock_Date, stock_Open, stock_Close, stock_High, stock_Low, stock_Volume]


'''
same as stock_preprocess_arr_list(ticker)
-> but for plotting candlesticks
'''
def stock_preprocess_candlestick(ticker):
    stock_df = fetch_yahoo_data(ticker)
    stock_Date = np.array(stock_df.index)
    stock_Date = np.array([datetime.datetime.strptime(str(t)[:10], '%Y-%m-%d').date() for t in stock_Date])
    stock_df['Date'] = stock_df.index.map(mdates.date2num)      # candlestick_ochl needs time in float days format
    stock_df_no_vol = stock_df[['Date', 'Open', 'Close', 'High', 'Low']]
    return [np.array(stock_df_no_vol.values), np.array(stock_df.Open), np.array(stock_df.Close), np.array(stock_df.Volume), stock_Date]


'''
take a string of ticker
check if it is ticker-name lookup or stock data lookup
return the processed string for calling yahoo APIs
'''
def tick_process(ticker):
    if ticker.lower() == 'hk' or ticker.lower() == 'us' or ticker.lower() == 'cn':
        return ticker.lower()
    else:
        try:
            num, country = ticker.split('.')
            country = country.upper()
            num = (4-len(num))*'0' + num
            return '{}.{}'.format(num, country)
        except:
            return ticker.upper()
