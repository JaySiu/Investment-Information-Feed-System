import time
import pandas as pd
import module_path as mp
from selenium import webdriver
from bs4 import BeautifulSoup

SLEEP_TIME = 1
COLS = ['Ticker','Name','Price', 'Turnover', 'Market_Cap', 'PE', 'Dividen', 'Security_type']
LINKS = ['https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=',
         'https://www.hkex.com.hk/Market-Data/Securities-Prices/Exchange-Traded-Products?sc_lang=',
         'https://www.hkex.com.hk/Market-Data/Securities-Prices/Real-Estate-Investment-Trusts?sc_lang=']
TABLE_NAMES = ['table_equities', 'table_etps', 'table_reits']
SECTURITY_TYPE = ['Equity', 'ETP', 'REIT']
COL_EXTRACT = [{'code': 0, 'name': 1, 'price': 2, 'turnover': 3, 'market': 4, 'pe': 5, 'dividend': 6},
               {'code': 0, 'name': 1, 'price': 2, 'aum': 4, 'dividend': 6},
               {'code': 0, 'name': 1, 'price': 2, 'turnover': 3, 'market': 4, 'pe': 5, 'change': 6}]
CHIN_NAME_MAP = {'00025': '其士國際', '00052': '大快活集團', '00078': '富豪國際', '00088': '大昌集團', '00092': '冠軍科技',
                 '00093': '添利', '00104': '冠亞商業集團', '00114': '興利集團', '00120': '四海國際', '00146': '太平地氈',
                 '00167': '萬威國際', '00186': '嘉域集團', '00211': '大凌集團', '00212': '南洋集團', '00213': '樂聲電子',
                 '00243': '品質國際', '00247': '尖沙咀置業', '00289': '永安', '00303': '偉易達', '00328': '愛高集團',
                 '00345': '維他奶國際', '00375': 'YGM貿易', '00495': '百利大', '00522': 'ASM太平洋', '00529': '新龍國際',
                 '00532': '王氏港建國際', '00592': '堡獅龍國際', '00610': '惠記集團', '00613': '渝港國際', '00697': '首長國際',
                 '00701': '北海集團', '00703': '佳景集團', '00730': '首長四方', '00752': '筆克遠東', '00758': '莊勝百貨集團',
                 '00759': 'CEC國際控股', '00765': '威發國際', '00767': '太平洋實業', '00805': '嘉能可', '00900': 'AEON信貸財務',
                 '01005': '美力時集團', '01098': '路勁', '01114': '華晨中國', '01116': '美亞控股', '01135': '亞洲衛星',
                 '01184': '時捷', '01221': '信和酒店', '01222': '宏安集團', '01323': '友川集團', '02011': '開易控股',
                 '02318': '中國平安保險', '06288': '迅銷', '06886': '華泰證券', '08160': '金滙教育', '08195': '樂亞國際',
                 '08215': '第一信用'}
driver = None

##### helpers ##################################################################

def check_suspended(tk):
    if tk.find('Suspended') >= 0:                   # cannot find: return -1
        return 'Yes'
    else:
        return 'No'


def process_ticker(tk):
    tk = tk.replace('Suspended', '').replace('IPO', '')
    return '0' * (5 - len(tk)) + str(tk)

def parse_table(df, text, sec_type, col_ext):
    print("Parsing {}...".format(sec_type))
    soup = BeautifulSoup(text, 'html.parser')       # create a soup tree object
    for tr in soup.find_all('tr'):
        row = ['-']*len(COLS)                       # a list of '-'
        for td in tr.find_all('td'):                # a list of <td> tags
            td_attr = td.attrs['class'][0]          # td_attr: code, name, etc
            if td_attr in col_ext.keys():
                row[col_ext[td_attr]] = td.get_text()
        row[-1] = sec_type                          # last column
        df.loc[len(df),:] = row                     # append row to the df
    return df


def crawl_hkex_tickers(lang):
    global driver
    if lang == 'en':
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(10)
        #driver.maximize_window()

    df = pd.DataFrame(columns=COLS)
    for i, link in enumerate(LINKS):
        driver.get(link + lang)
        time.sleep(SLEEP_TIME*2)

        stock_code = driver.find_element_by_xpath("//th[@class='text']")     # find the "Stock Code" button
        stock_code.click()                   # Click the button to sort in asc order
        time.sleep(SLEEP_TIME)
        try:
            show_items = driver.find_element_by_xpath("//div[@class='loadmore_update dropdown']")    # find the dropdown at the bottom
            show_items.click()
            time.sleep(SLEEP_TIME)
            show_items = driver.find_element_by_xpath("//div[@class='select_items']/div[3]")     # select 100 items, i.e. the 3rd div
            show_items.click()
            time.sleep(SLEEP_TIME)
        except:
            pass

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
        txt = source_code[data_index-11:end_index]          # -11 moves the index to '<' of <tr class=...>
        df = parse_table(df, txt, SECTURITY_TYPE[i], COL_EXTRACT[i])

    if lang == 'zh-HK':
        driver.quit()

    return df


################################################################################

def get_ticker_list():
    print("Fetching ticker information list from HKEX...")

    df_en = crawl_hkex_tickers('en')
    df_zh = crawl_hkex_tickers('zh-HK')

    df_en['Chin_Name'] = df_zh.Name
    df = df_en[['Ticker','Name', 'Chin_Name', 'Price', 'Turnover', 'Market_Cap', 'PE', 'Dividen', 'Security_type']]

    df['Suspended'] = df.Ticker.apply(check_suspended)
    df.Ticker = df.Ticker.apply(process_ticker)          # this statement must run before Chinese name mapping

    for k in CHIN_NAME_MAP.keys():
        idx = df.index[df.Ticker == k].values            # return the index of the row with 'Ticker'==k
        df.loc[idx, 'Chin_Name'] = CHIN_NAME_MAP.get(k)  # get value of key k

    df = df.sort_values(by='Ticker')

    print("Saving ticker information...")
    df.to_csv(mp.DIR_DATA_NEWS + 'ticker_info_list_hkex.csv', index=False, encoding='utf_8_sig')
    time.sleep(SLEEP_TIME)
    print("Done")
    print("\n")
