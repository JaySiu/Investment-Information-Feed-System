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
    if os.path.exists(r'\\ifsf03\team\RDTeam\Research\Project\iifv2\data\^HSI.csv'):
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
    source_code = driver.page_source        # $chcp 65001 command may be needed
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


def retrieve_HSI_data():
    return np.array(pd.read_csv(mp.dir_data + '^HSI.csv').Close.apply(remove_comma), dtype='f8')


def calculate_macd(close_prices, fast=12, slow=26, signal=9):
    print("Calculating MACD...")
    print("Fast: {}-days; Slow: {}-days; Signal: {}-days".format(fast, slow, signal))
    print("Select your Moving Average type:")
    type = input("(SMA,EMA,WMA,DEMA,TEMA,TRIMA,KAMA,MAMA,T3)").upper()
    avg_fast = talib.MA(close_prices, timeperiod=fast, matype=ma_type[type])
    avg_fast = remove_nan(avg_fast)
    #print(avg_fast)
    avg_slow = talib.MA(close_prices, timeperiod=slow, matype=ma_type[type])
    avg_slow = remove_nan(avg_slow)
    #print(avg_slow)
    avg_signal = talib.MA(close_prices, timeperiod=signal, matype=ma_type[type])
    avg_signal = remove_nan(avg_signal)
    #print(avg_signal)

    #fig = plt.figure()
    #ax = fig.add_subplot(1,1,1)
    plt.plot(close_prices)
    plt.plot(avg_fast)
    plt.plot(avg_slow)
    plt.plot(avg_signal)
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
    print("\n")
    if update == 'y':
        if fast == 'd':
            calculate_macd(update_HSI_data())
        else:
            slow = input("Slow period: (days)")
            signal = input("Signal: (days)")
            calculate_macd(update_HSI_data(), fast, slow, signal)
    elif update == 'n' and check_HSI_data_exist():
        if fast == 'd':
            calculate_macd(retrieve_HSI_data())
        else:
            slow = input("Slow period: (days)")
            signal = input("Signal: (days)")
            calculate_macd(retrieve_HSI_data(), fast, slow, signal)
    elif update == 'n' and not check_HSI_data_exist():
        print("No existing data!")
        if fast == 'd':
            calculate_macd(update_HSI_data())
        else:
            slow = input("Slow period: (days)")
            signal = input("Signal: (days)")
            calculate_macd(update_HSI_data(), fast, slow, signal)


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
