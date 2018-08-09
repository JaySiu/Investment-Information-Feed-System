import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

SLEEP_TIME = 1
COLS = ['Ticker','Name','Price', 'Turnover', 'Market_Cap', 'PE', 'Dividen', 'Security_type']
LINKS = ['https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=',\
         'https://www.hkex.com.hk/Market-Data/Securities-Prices/Exchange-Traded-Products?sc_lang=',\
         'https://www.hkex.com.hk/Market-Data/Securities-Prices/Real-Estate-Investment-Trusts?sc_lang=']
TABLE_NAMES = ['table_equities', 'table_etps', 'table_reits']
SECTURITY_TYPE = ['Equity', 'ETP', 'REIT']
COL_EXTRACT = [{'code':0, 'name':1, 'price':2, 'turnover':3, 'market':4, 'pe':5, 'dividend':6},\
               {'code':0, 'name':1, 'price':2, 'aum':4, 'dividend':6},\
               {'code':0, 'name':1, 'price':2, 'turnover':3, 'market':4, 'pe':5, 'change':6}]

##### helpers ##################################################################

def parse_table(text, sec_type, col_ext):
    pass


def crawl_data(lang):
    for i, link in enumerate(LINKS):
        driver.get(link + lang)
        time.sleep(SLEEP_TIME)

        stock_code = driver.find_element_by_xpath("//th[@class='text']")     # find the "Stock Code" button
        stockcode.click()                   # Click the button to sort in asc order
        time.sleep(SLEEP_TIME)

        show_items = driver.find_element_by_xpath("//div[@class='loadmore_update dropdown']")    # find the dropdown at the bottom
        show_items.click()
        time.sleep(SLEEP_TIME)
        show_items = driver.find_element_by_xpath("//div[@class='select_items']/div[3]")     # select 100 items, i.e. the 3rd div
        show_items.click()
        time.sleep(SLEEP_TIME)

        for j in range(40):                 # keep clicking "LOAD MORE"
            try:
                load_more = driver.find_element_by_class_name('load')
                load_more.click()
                time.sleep(SLEEP_TIME)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")     # scroll to the bottom of the window
                time.sleep(SLEEP_TIME)
            except:
                break
        time.sleep(SLEEP_TIME)

        source_code = driver.page_source             # get the page source code
        start_index = source_code.find(TABLE_NAMES[i])    # get starting index number of the tables
        data_index = source_code.find('datarow', start_index)   # get the starting index of the datarows
        end_index = source_code.find('</tr></tbody></table>', data_index)
        txt = source_code[midLoc-11:endLoc]          # -11 moves the index to '<' of <tr class=...>
        return parse_table(txt, SECTURITY_TYPE[i], COL_EXTRACT[i])


################################################################################

def get_ticker_list():
    print("*******************************************************")
    print("Fetching ticker information list from HKEX...")

    driver = webdriver.Chrome()
    time.sleep(SLEEP_TIME)
    df_en = crawl_data('en')
    df_zh = crawl_data('zh-HK')
