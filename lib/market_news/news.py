import os
import module_path as mp
from ticker_list import get_ticker_list
from aastocks import get_aastocks_news
from analyze_news import analyze_news

def get_news():
    print("*******************************************************")
    print("Do you want to update ticker list from HKEX? (It may take a while)")
    update = input("[y/n] ")
    if update.lower() == 'y':
        get_ticker_list()
        get_aastocks_news()
        analyze_news()
    elif update.lower() == 'n':
        if os.path.exists(mp.DIR_DATA_NEWS + 'ticker_info_list_HKEX.csv'):
            print("Ticker list information exists")
            get_aastocks_news()
            analyze_news()
        else:
            print("No ticker list information exists!")
            get_ticker_list()
            get_aastocks_news()
            analyze_news()
    else:
        print("Invalid Input!")
