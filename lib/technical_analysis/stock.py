import os
import re
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

'''
save the plot to data/plots directory

def save_plot(type, ticker):
    Print("Saving the plot...")
    plt.savefig(mp.dir_data_plots + type + ' - ' + check_all_ticker(ticker)[0] + '.jpeg')
'''


'''
check the last modification date if the stock data exists
'''
def check_modi_date(ticker):
    mtime = os.path.getmtime(mp.dir_data_stocks + '{}.csv'.format(ticker))
    mtime = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    mtime = datetime.datetime.strptime(mtime, '%Y-%m-%d')
    now = datetime.datetime.today()
    if mtime.date() < now.date():
        return [True, mtime]
    else:
        return [False, mtime]

'''
call the yahoo finance API to download data
save the data to .csv file
'''
def yahoo_api(ticker):
    print("!-- API may return an error, just re-run the program --!")
    end = datetime.datetime.today()
    start = end - datetime.timedelta(weeks=52)
    stock_df = yf.download(ticker, start=start, end=end)    # return a DataFrame
    time.sleep(SLEEP_TIME)
    #stock_df_cvs = stock_df
    #stock_Date = np.array(stock_df.index)
    #stock_df_cvs['Index'] = stock_Date
    #stock_df['Date'] = np.array([datetime.datetime.strptime(str(t)[:10], '%Y-%m-%d').date() for t in stock_Date])
    #stock_df = stock_df[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
    stock_df_save = stock_df.sort_values(by='Date', ascending=False)
    stock_df_save.to_csv(mp.dir_data_stocks + '{}.csv'.format(ticker), index=True, encoding='utf_8_sig')
    time.sleep(SLEEP_TIME*3)
    return stock_df


'''
take a string of ticker
call yahoo_api() function
return a copy of the DataFrame with added 'Date' column (from the index)
improve performance by checking if some data exists
'''
def fetch_yahoo_data(ticker):
    name = check_all_ticker(ticker)[0]
    print("Checking {}'s data...".format(name))
    if check_stock_data_exist(ticker):
        print("Has old data: %s" % True)
        modi = check_modi_date(ticker)
        if modi[0] == True:
            print("Last updated time for {}: {}".format(name, modi[1]))
            os.remove(mp.dir_data_stocks + '{}.csv'.format(ticker))
            time.sleep(SLEEP_TIME)
            print("Fetching {}'s data...".format(name))
            stock_df = yahoo_api(ticker)
        else:
            print("Data is up-to-date")
            stock_df = pd.read_csv(mp.dir_data_stocks + '{}.csv'.format(ticker), index_col='Date')
            stock_df = stock_df.sort_values(by='Date', ascending=True)
    else:
        print("Has old data: %s" % False)
        print("Fetching {}'s data...".format(name))
        stock_df = yahoo_api(ticker)

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
    try:
        return [ticker_dict[ticker], True]
    except:
        return ["{}'s data not found!".format(ticker), False]


'''
take a string of ticker
check if the ticker's .csv file already exists
if exists, remove the file
'''
def check_stock_data_exist(ticker):
    if os.path.exists(mp.dir_data_stocks + '{}.csv'.format(ticker)):
        return True
    else:
        return False


'''
take a string of ticker
return a list of the ticker's data coulmns as numpy arrays
[0stock_Date, 1stock_Open, 2stock_Close, 3stock_High, 4stock_Low, 5stock_Volume]
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
[np.array(stock_df_no_vol.values), stock_Open, stock_Close, stock_Volume, stock_Date]
-> but for plotting candlesticks
'''
def stock_preprocess_candlestick(ticker):
    stock_df = fetch_yahoo_data(ticker)
    stock_Date = np.array(stock_df.index)
    stock_Date = np.array([datetime.datetime.strptime(str(t)[:10], '%Y-%m-%d').date() for t in stock_Date])
    stock_df['Date'] = np.array(pd.Series(stock_Date).map(mdates.date2num))      # candlestick_ochl needs time in float days format
    stock_df_no_vol = stock_df[['Date', 'Open', 'Close', 'High', 'Low']]
    return [np.array(stock_df_no_vol.values), np.array(stock_df.Open), np.array(stock_df.Close), np.array(stock_df.Volume), stock_Date]


'''
take a string of ticker
check if it is ticker-name lookup or stock data lookup
return the processed string for calling yahoo APIs
(only support HK, CN and US)
'''
def tick_process(ticker):
    dot_patt = re.compile('^[0-9]+\.[a-zA-Z]+$')
    plain_patt = re.compile('^[a-zA-Z]+$')
    is_dot = dot_patt.match(ticker)
    is_plain = plain_patt.match(ticker)

    if ticker.lower() == 'hk' or ticker.lower() == 'us' or ticker.lower() == 'cn':
        return ticker.lower()
    elif is_dot != None:
        num, country = ticker.split('.')
        country = country.upper()
        num = (4-len(num))*'0' + num
        new_tk = '{}.{}'.format(num, country)
        if check_all_ticker(new_tk)[1] == True:
            return new_tk
        else:
            return ''
    elif is_plain != None:
        if check_all_ticker(ticker.upper())[1] == True:
            return ticker.upper()
        else:
            return ''
    else:
        return ''
