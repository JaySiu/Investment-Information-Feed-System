import re
import pandas as pd
import module_path as mp
import mk_user_portfolio as mkup

SLEEP_TIME = 1
COLS = ['Cus_ID', 'Ticker', 'Date', 'Time', 'Link', 'Title', 'Content']

##### helpers ##################################################################

def check_news_content(ticker, news_df):
    num, country = ticker.split('.')
    num = (5-len(num))*'0' + num
    pattern = r'\(' + num + r'\.' + country + r'\)'
    ticker_patt = re.compile(pattern)
    indices = []

    for idx, row in news_df.iterrows():
        relate_to_customer = ticker_patt.search(row.Content)
        if relate_to_customer != None:
            indices.append(idx)
    return indices


def portfolio_news_mapping(cus_id, portfolio, news_source):
    print("Mapping {} news with customer's portfolio...".format(news_source.upper()))
    news_df = pd.read_csv(mp.DIR_DATA_NEWS + news_source + '_news.csv')
    news_list = {}
    map_df = pd.DataFrame(columns=COLS)

    for tk in portfolio:
        news_list[tk] = check_news_content(tk, news_df)
        if news_list[tk] != []:
            for idx in news_list[tk]:
                map_df.loc[len(map_df),2:] = news_df.iloc[idx,:]
                map_df.loc[len(map_df)-1,'Ticker'] = tk
        else:
            map_df.loc[len(map_df),2:] = '-'*(map_df.shape[1]-2)
            map_df.loc[len(map_df)-1,'Ticker'] = tk

    map_df['Cus_ID'] = cus_id
    map_df = map_df[['Cus_ID', 'Ticker', 'Date', 'Time', 'Title', 'Content']]
    map_df = map_df.set_index(['Cus_ID', 'Ticker'])
    print("Saving news related to the customer...")
    map_df.to_csv(mp.DIR_DATA_CUSTOMERS + 'customer_related_news.csv', index=True, encoding='utf_8_sig')
    print("Done\n")


################################################################################

def analyze_news():
    print("*******************************************************")
    print("Enter your client\'s id (number only):")
    cus_id = input()
    cus_ticker_list = mkup.get_client_tickers(cus_id)
    if cus_ticker_list == None or cus_ticker_list == []:
        print("Customer data not found!")
        cus_ticker_list = []
    print("\n")

    if cus_ticker_list != []:
        portfolio_news_mapping('scb_' + cus_id, cus_ticker_list, 'aastocks')
