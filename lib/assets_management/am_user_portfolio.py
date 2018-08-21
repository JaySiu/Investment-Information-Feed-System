import stock
import numpy as np
import pandas as pd
import module_path as mp
from selenium import webdriver
from bs4 import BeautifulSoup

USTD = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=billrates'

def get_closes(ticker_list):
    return [stock.fetch_yahoo_data(tk, 208)['Adj Close'] for tk in ticker_list]

'''
return a list of expected returns (float) of the assets
'''
def get_expected_returns(closes):
    expected_return_list = []
    for c in closes:
        expected_return_list.append(np.mean(c.pct_change(periods=30).dropna(axis=0)))
    return np.asmatrix(expected_return_list)


def get_var_cov_matrix(closes):
    var_cov_matrix = []
    min_len = 9999
    for c in closes:
        if len(c) < min_len:
            min_len = len(c)
        var_cov_matrix.append(np.array(c).astype(float))
    for i, arr in enumerate(var_cov_matrix):
        if len(arr) != min_len:
            var_cov_matrix[i] = arr[:min_len]
    var_cov_matrix = np.cov(var_cov_matrix)
    return np.asmatrix(var_cov_matrix)


def get_client_tickers(cus_id):
    id = 'scb_' + cus_id
    customers_df = pd.read_csv(mp.DIR_DATA_CUSTOMERS + 'customer_trade_book.csv')
    customers_df = customers_df[['ID', 'Symbol', 'Portfolio_Value']]
    customers_df = customers_df[customers_df.ID == id]
    customers_df = customers_df[customers_df.Portfolio_Value > 0]
    ticker_list = list(set(customers_df['Symbol']))
    if len(ticker_list) > 0:
        ticker_list = [(4-len(str(tk)))*'0' + str(tk) +'.HK' for tk in ticker_list]
        remove_tk_list = []
        print("Customer {} has the following equities in his/her portfolio:".format(id))
        for i, tk in enumerate(ticker_list):
            found = stock.check_all_ticker(tk)
            if found[1] == True:
                print(str(i+1) + ')', tk + ' - ' + found[0])
            else:
                print(str(i+1) + ')', found[0])
                remove_tk_list.append(tk)
        for tk in remove_tk_list:
            ticker_list.remove(tk)
        print("\n")
        return ticker_list
    else:
        return None


def get_risk_free_rate():
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(10)
    driver.get(USTD)
    source_code = driver.page_source
    start_index = source_code.find('52 WEEKS')
    end_index = source_code.find('Daily Treasury Bill Rates', start_index)
    driver.quit()
    soup = BeautifulSoup(source_code[start_index+18:end_index], "lxml")
    return float(soup.find_all('td')[3].get_text())
