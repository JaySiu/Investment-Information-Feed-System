'''
Moving Average Convergence/Divergence (MACD)

(no restrictive checking on user inputs)
'''

import os
import time
import datetime
import pandas as pd
import sys
import numpy as np
import module_path as mp
import talib
import matplotlib.pyplot as plt
from selenium import webdriver
from bs4 import BeautifulSoup

#import quandl
#pd.core.common.is_list_like = pd.api.types.is_list_like
#import pandas_datareader.data as web

#quandl.ApiConfig.api_key = ""
SLEEP_TIME = 1
df = pd.DataFrame(columns = ['Date', 'Open',  'High', 'Low', 'Close', 'Adj Close', 'Volume'])
ma_type = {'SMA': 0 , 'EMA': 1, 'WMA': 2, 'DEMA': 3, 'TEMA': 4, 'TRIMA': 5, 'KAMA': 6, 'MAMA': 7, 'T3': 8}

##### helpers ##################################################################

def check_HSI_data_exist():
    if os.path.exists('data/^HSI.csv'):
        return True
    else:
        return False


def remove_comma(str):
    return str.replace(',', '')


def remove_nan(arr):
    return arr[~np.isnan(arr)]


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
    for i in range(10):
        try:
            print(".")
            driver.execute_script("window.scrollTo(0, 200000);")
            time.sleep(SLEEP_TIME)
        except:
            break

    time.sleep(SLEEP_TIME)
    source_code = driver.page_source        # $chcp 65001 command may be needed for pritning
    start_index = source_code.find('Download Data')
    table_index = source_code.find('<table class=', start_index)
    end_index = source_code.find('</tr></tfoot></table>', table_index)
    text = source_code[table_index:end_index+21]
    driver.quit()

    global df
    close_prices = np.array(parse_HSI_data(text), dtype='f8')
    print("Saving...")
    print("\n")
    df.to_csv(mp.dir_data + '^HSI.csv', index=False, encoding='utf_8_sig')
    time.sleep(SLEEP_TIME*3)
    return close_prices


def retrieve_HSI_Date():
    return np.array(pd.read_csv(mp.dir_data + '^HSI.csv').Date)


def retrieve_HSI_Close():
    return np.array(pd.read_csv(mp.dir_data + '^HSI.csv').Close.apply(remove_comma), dtype='f8')


def calculate_macd(close_prices, fast=12, slow=26, signal=9):
    print("Calculating MACD...")
    print("Fast: {}-days; Slow: {}-days; Signal: {}-days".format(fast, slow, signal))
    print("Select your Moving Average type:")
    type = input("(SMA,EMA,WMA,DEMA,TEMA,TRIMA,KAMA,MAMA,T3)").upper()
    avg_fast = talib.MA(close_prices, timeperiod=fast, matype=ma_type[type])
    #avg_fast = remove_nan(avg_fast)
    #print(avg_fast)
    avg_slow = talib.MA(close_prices, timeperiod=slow, matype=ma_type[type])
    #avg_slow = remove_nan(avg_slow)
    #print(avg_slow)
    macd = avg_fast - avg_slow
    avg_signal = talib.MA(macd, timeperiod=signal, matype=ma_type[type])
    #avg_signal = remove_nan(avg_signal)
    #print(avg_signal)
    histogram = macd - avg_signal


    plot_HSI_MACD(close_prices, avg_fast, avg_slow, avg_signal, macd, histogram, fast, slow, signal, type)


def plot_HSI_MACD(close_prices, avg_fast, avg_slow, avg_signal, macd, histogram, fast, slow, signal, type):
    #date_HSI = retrieve_HSI_Date()
    #print(date_HSI)
    fig, ax_list = plt.subplots(2, 2)
    plt.suptitle('MACD-related plots using {}'.format(type), fontsize = 20, fontweight='bold')

    ax_list[0][0].set_title('{}-days and {}-days Moving Average'.format(fast, slow), fontstyle='italic')
    ax_list[0][0].plot(close_prices, label='^HSI')
    ax_list[0][0].plot(avg_fast, label=str(fast)+'-days(fast)')
    ax_list[0][0].plot(avg_slow, label=str(slow)+'-days(slow)')
    ax_list[0][0].legend()
    ax_list[0][0].grid(True)

    ax_list[0][1].set_title('MACD/DIF', fontstyle='italic')
    ax_list[0][1].plot(macd, label='{}-days - {}-days'.format(fast, slow), color='xkcd:purple')
    ax_list[0][1].legend()
    ax_list[0][1].grid(True)

    ax_list[1][0].set_title('MACD/DIF & {}day-Signal', fontstyle='italic')
    ax_list[1][0].plot(macd, label='MACD/DIF', color='xkcd:purple')
    ax_list[1][0].plot(avg_signal, label='Signal', color='xkcd:orange')
    ax_list[1][0].legend()
    ax_list[1][0].grid(True)

    ax_list[1][1].set_title('MACD Histogram', fontstyle='italic')
    ax_list[1][1].hist(remove_nan(histogram), label='MACD/DIF - Signal', color='C9')
    ax_list[1][1].legend()
    ax_list[1][1].grid(True)

    plt.show()


################################################################################

def macd_HSI():
    print("*******************************************************")
    print("Running MACD...")
    #end = datetime.datetime.today()
    #start = end - datetime.timedelta(weeks=52)
    update = input("Do you want to update HSI data? [y/n]").lower()
    print("Fast period: (days)")
    print("[Enter d to use default: 12(fast), 26(slow), 9(signal)]")
    fast = input().lower()
    if update == 'y':
        if fast == 'd':
            print("\n")
            calculate_macd(update_HSI_data())
        else:
            slow = input("Slow period: (days)")
            signal = input("Signal: (days)")
            print("\n")
            calculate_macd(update_HSI_data(), int(fast), int(slow), int(signal))
    elif update == 'n' and check_HSI_data_exist():
        if fast == 'd':
            print("Fetching existing data...")
            print("\n")
            calculate_macd(retrieve_HSI_Close())
        else:
            slow = input("Slow period: (days)")
            signal = input("Signal: (days)")
            print("Fetching existing data...")
            print("\n")
            calculate_macd(retrieve_HSI_Close(), int(fast), int(slow), int(signal))
    elif update == 'n' and not check_HSI_data_exist():
        if fast == 'd':
            print("No existing data!")
            print("\n")
            calculate_macd(update_HSI_data())
        else:
            slow = input("Slow period: (days)")
            signal = input("Signal: (days)")
            print("No existing data!")
            print("\n")
            calculate_macd(update_HSI_data(), int(fast), int(slow), int(signal))
    else:
        print("Error!")


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
