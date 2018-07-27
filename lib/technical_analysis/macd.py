'''
Moving Average Convergence/Divergence (MACD)
Results for HSI may not be very accurate because of the sparse data source

(no restrictive checking on user inputs)
'''

import os
import time
import pandas as pd
import sys
import numpy as np
import module_path as mp
import talib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#import pandas_datareader.data as pdr
import fix_yahoo_finance as yf
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime

#import quandl
#pd.core.common.is_list_like = pd.api.types.is_list_like


#quandl.ApiConfig.api_key = ""
SLEEP_TIME = 1
df = pd.DataFrame(columns = ['Date', 'Open',  'High', 'Low', 'Close', 'Adj Close', 'Volume'])
ma_type = {'SMA': 0 , 'EMA': 1, 'WMA': 2, 'DEMA': 3, 'TEMA': 4, 'TRIMA': 5, 'KAMA': 6, 'MAMA': 7, 'T3': 8}
stock_Date = ''
ticker_dict_country = {}

##### helpers ##################################################################

def check_stock_data_exist(ticker):
    if os.path.exists('data/{}.csv'.format(ticker)):
        os.remove('data/{}.csv'.format(ticker))
        return True
    else:
        return False


def check_all_ticker(ticker):
    ticker_df = pd.read_csv(mp.dir_ta + 'Yahoo_Ticker_Symbols_Sep2017.csv')
    ticker_dict = dict(zip(ticker_df.Ticker, ticker_df.Name))
    return ticker_dict[ticker]

def check_ticker_by_country(country):
    ticker_df = pd.read_csv(mp.dir_ta + 'Yahoo_Ticker_Symbols_Sep2017.csv')
    ticker_df = ticker_df[ticker_df.Country == country].sort_values(by='Ticker')
    global ticker_dict_country
    ticker_dict_country = dict(zip(ticker_df.Ticker, ticker_df.Name))
    keys = list(ticker_dict_country.keys())
    keys.sort()
    for k in keys:
        print(k, ticker_dict_country[k])            # $chcp 65001 may be needed


def check_HSI_data_exist():
    if os.path.exists('data/^HSI.csv'):
        return True
    else:
        return False


def remove_comma(str):
    return str.replace(',', '')


#def remove_nan(arr):
#    return arr[~np.isnan(arr)]


def parse_HSI_data(text):
    print("Parsing HSI data...")
    global df
    soup = BeautifulSoup(text, 'html.parser')
    for tr in soup.find_all('tr'):
        row = ['-']*(df.shape[1])
        for i, td in enumerate(tr.find_all('td')):
            row[i] = td.get_text()
        df.loc[len(df),:] = row

    df = df[df.Close != '-']

    print("{} data entries parsed".format(len(df)))
    return df.Close.apply(remove_comma)


def update_HSI_data():
    print("Getting HSI data...")
    print("!-- Please ignore handshake errors --!")
    print("!-- Wait or just re-run the program --!")

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://finance.yahoo.com/quote/%5EHSI/history?p=%5EHSI')
    time.sleep(SLEEP_TIME*3)
    for i in range(5):
        try:
            print(".")
            driver.execute_script("window.scrollTo(0, 200000);")
            time.sleep(SLEEP_TIME*2)
        except:
            break

    time.sleep(SLEEP_TIME)
    source_code = driver.page_source        # $chcp 65001 command may be needed for pritning
    start_index = source_code.find('Download Data')
    table_index = source_code.find('<table class=', start_index)
    end_index = source_code.find('</tr></tfoot></table>', table_index)
    text = source_code[table_index:end_index+21]
    driver.quit()

    close_prices = np.array(parse_HSI_data(text), dtype='f8')
    print("Saving...")
    print("\n")
    global df
    df.to_csv(mp.dir_data + '^HSI.csv', index=False, encoding='utf_8_sig')
    time.sleep(SLEEP_TIME*3)
    arr_date = retrieve_HSI_Date()      # in desc order
    return [arr_date, close_prices]


def retrieve_HSI_Date():
    date = np.array(pd.read_csv(mp.dir_data + '^HSI.csv').Date)
    return np.array([datetime.datetime.strptime(t, '%b %d, %Y').date() for t in date])


def retrieve_HSI_Close():
    return np.array(pd.read_csv(mp.dir_data + '^HSI.csv').Close.apply(remove_comma), dtype='f8')


def calculate_macd(arr_date, close_prices, ticker, fast=12, slow=26, signal=9):
    print("Calculating MACD...")
    print("Fast: {}-days; Slow: {}-days; Signal: {}-days".format(fast, slow, signal))
    print("Select your Moving Average type:")
    type = input("(SMA,EMA,WMA,DEMA,TEMA,TRIMA,KAMA,MAMA,T3)").upper()
    #print(close_prices)        # in desc order
    avg_fast = talib.MA(close_prices, timeperiod=fast, matype=ma_type[type])    # in desc order
    #print(avg_fast)
    avg_slow = talib.MA(close_prices, timeperiod=slow, matype=ma_type[type])    # in desc order
    #print(avg_slow)
    macd, macd_signal, histogram = talib.MACD(close_prices, fastperiod=fast, slowperiod=slow, signalperiod=signal)

    plot_HSI_MACD(arr_date, close_prices, avg_fast, avg_slow, macd, macd_signal, histogram, ticker, fast, slow, signal, type)


def plot_HSI_MACD(arr_date, close_prices, avg_fast, avg_slow, macd, macd_signal, histogram, ticker, fast=12, slow=26, signal=9, type='EMA'):
    fig, ax_list = plt.subplots(2, 2)
    if ticker == 'HSI':
        plt.suptitle('MACD-related plots of {}'.format(ticker), fontsize = 20, fontweight='bold')
    else:
        plt.suptitle('MACD-related plots of {}({})'.format(check_all_ticker(ticker), ticker), fontsize = 20, fontweight='bold')

    ax_list[0][0].set_title('{}-days and {}-days {}'.format(fast, slow, type), fontstyle='italic')
    ax_list[0][0].plot(arr_date, close_prices, label='^HSI', color='black')
    ax_list[0][0].plot(arr_date, avg_fast, label=str(fast)+'-days(fast)')
    ax_list[0][0].plot(arr_date, avg_slow, label=str(slow)+'-days(slow)')

    ax_list[0][1].set_title('MACD/DIF (EMA)', fontstyle='italic')
    ax_list[0][1].plot(arr_date, macd, label='{}-days - {}-days'.format(fast, slow), color='xkcd:purple')
    ax_list[0][1].axhline(y=0, color='red')

    ax_list[1][0].set_title('MACD/DIF & {}day-Signal'.format(signal), fontstyle='italic')
    ax_list[1][0].plot(arr_date, macd, label='MACD/DIF', color='xkcd:purple')
    ax_list[1][0].plot(arr_date, macd_signal, label='Signal', color='xkcd:orange')
    ax_list[1][0].fill_between(arr_date, histogram, label='MACD/DIF - Signal', color='gray')
    ax_list[1][0].axhline(y=0, color='red')

    ax_list[1][1].set_title('MACD Histogram', fontstyle='italic')
    ax_list[1][1].fill_between(arr_date, histogram, label='MACD/DIF - Signal', color='C9')
    ax_list[1][0].axhline(y=0, color='red')

    for row in range(len(ax_list)):
        for col in range(len(ax_list[0])):
            ax_list[row][col].legend()
            ax_list[row][col].grid(True)
            ax_list[row][col].minorticks_on()
            ax_list[row][col].tick_params(axis='x',which='minor',bottom='off')
            ax_list[row][col].xaxis.set_major_locator(mdates.MonthLocator())
            ax_list[row][col].xaxis.set_major_formatter(mdates.DateFormatter('%y-%b'))
            if ticker == 'HSI':
                for major_tick in ax_list[row][col].xaxis.get_ticklabels():
                    major_tick.set_rotation(20)
            else:
                for major_tick in ax_list[row][col].xaxis.get_ticklabels():
                    major_tick.set_rotation(43)

    plt.tight_layout()
    plt.show()


################################################################################

def macd_stocks(ticker):
    print("Fetching {}'s data...".format(check_all_ticker(ticker)))
    end = datetime.datetime.today()
    start = end - datetime.timedelta(weeks=104)
    global stock_Date
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


    print("[Enter d to use default: 12(fast), 26(slow), 9(signal)]")
    fast = input("Fast period: (days)").lower()
    if fast == 'd':
        print("\n")
        calculate_macd(stock_Date, stock_Close, ticker)
    elif fast.isdigit():
        slow = input("Slow period: (days)")
        signal = input("Signal: (days)")
        print("\n")
        calculate_macd(stock_Date, stock_Close, ticker, int(fast), int(slow), int(signal))
    else:
        print("Error!")


def macd_HSI():
    update = input("Do you want to update HSI data? [y/n]").lower()
    print("[Enter d to use default: 12(fast), 26(slow), 9(signal)]")
    fast = input("Fast period: (days)").lower()
    if update == 'y':
        if fast == 'd':
            print("\n")
            calculate_macd(*update_HSI_data(), 'HSI')
        else:
            slow = input("Slow period: (days)")
            signal = input("Signal: (days)")
            print("\n")
            calculate_macd(*update_HSI_data(), int(fast), 'HSI', int(slow), int(signal))
    elif update == 'n' and check_HSI_data_exist():
        if fast == 'd':
            print("Fetching existing data...")
            print("\n")
            calculate_macd(retrieve_HSI_Date(), retrieve_HSI_Close(), 'HSI')
        else:
            slow = input("Slow period: (days)")
            signal = input("Signal: (days)")
            print("Fetching existing data...")
            print("\n")
            calculate_macd(retrieve_HSI_Date(), retrieve_HSI_Close(), 'HSI', int(fast), int(slow), int(signal))
    elif update == 'n' and not check_HSI_data_exist():
        if fast == 'd':
            print("No existing data!")
            print("\n")
            calculate_macd(*update_HSI_data(), 'HSI')
        else:
            slow = input("Slow period: (days)")
            signal = input("Signal: (days)")
            print("No existing data!")
            print("\n")
            calculate_macd(*update_HSI_data(), 'HSI', int(fast), int(slow), int(signal))
    else:
        print("Error!")





def macd():
    print("*******************************************************")
    print("Running MACD...")
    print("Get MACD on:")
    print("1) Hang Seng Index")
    print("2) Stocks")
    print("3) User Portfolio")
    ope = input()
    if ope == '1':
        macd_HSI()
    elif ope == '2':
        print("Stock ticker(e.g. 0001.HK): ")
        ticker = input("[Type 'hk' for Hong Kong tickers; 'us' for USA; 'cn' for China]")
        if ticker.lower() == 'hk':
            check_ticker_by_country('Hong Kong')
        elif ticker.lower() == 'us':
            check_ticker_by_country('USA')
        elif ticker.lower() == 'cn':
            check_ticker_by_country('China')
        else:
            print("\n")
            macd_stocks(ticker)

    print("Finish")

'''
    # delete the old file
    if os.path.exists(r'\\ifsf03\team\RDTeam\Research\Project\iifv2\data\^HSI.csv'):
        os.remove(r'\\ifsf03\team\RDTeam\Research\Project\iifv2\data\^HSI.csv')
    chromeOptions = webdriver.ChromeOptions()
    download_path = r'\\ifsf03\team\RDTeam\Research\Project\iifv2\data'
    prefs = {'download.default_directory' : download_path}
    chromeOptions.add_experimental_option('prefs',prefs)
    chromeOptions.add_argument('--ignore-certificate-errors')
    chromeOptions.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chromeOptions)
    driver.get('https://finance.yahoo.com/quote/%5EHSI/history?p=%5EHSI')
    download = driver.find_element_by_link_text('Download Data')
    download.click()
    time.sleep(2)
    driver.quit()
'''

'''
if __name__ == '__main__':
    macd()
'''
