'''
Bollinger Bands (B-Bands)
'''

import talib
import stock
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from ta_user_portfolio import get_client_tickers
from mpl_finance import candlestick_ochl, volume_overlay

##### helper ###################################################################

def cal_plot_bband(ticker):
    print("Calculating B-Bands...")
    stock_data = stock.stock_preprocess_candlestick(ticker)
    upper, middle, lower = talib.BBANDS(stock_data[2], matype=talib.MA_Type.SMA)

    ##### plotting
    fig, ax_list = plt.subplots(2, 1, figsize=(15,15))
    plt.suptitle('Bollinger Bands of {}({})'.format(stock.check_all_ticker(ticker)[0], ticker), fontsize = 20, fontweight='bold')

    candlestick_ochl(ax_list[0], stock_data[0], width=0.8, colorup='#53B987', colordown='#EB4D5C')
    ax_list[0].xaxis.set_major_locator(mdates.MonthLocator())
    ax_list[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d'))
    ax_list[0].get_xaxis().set_visible(False)
    volume_overlay(ax_list[1], *stock_data[1:4], width=0.8, colorup='#53B987', colordown='#EB4D5C')
    #ax_list[1].xaxis.set_major_locator(mdates.MonthLocator())
    #ax_list[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d'))
    ax_list[1].set_xticks(range(0, len(stock_data[4]), 30))
    ax_list[1].set_xticklabels(stock_data[4][::30])

    ax_list[0].plot(stock_data[4], upper, color='#85C0C0')
    ax_list[0].plot(stock_data[4], middle, label='20-SMA', color='#AC7878')
    ax_list[0].plot(stock_data[4], lower, color='#85C0C0')
    ax_list[0].fill_between(stock_data[4], upper, lower, color='#F3F9F9')

    for i in range(2):
        ax_list[i].minorticks_on()
        ax_list[i].tick_params(axis='x',which='minor',bottom='off')

    ax_list[0].legend()
    plt.setp(plt.gca().get_xticklabels())
    fig.tight_layout()
    fig.subplots_adjust(hspace=0, top=0.95)
    #plt.show()
    stock.save_plot('BBANDS', ticker)

'''
Other ways to plot:
    1):
    # set up subplot grid
    gridspec.GridSpec(3,3)
    plt.subplot2grid((3,3), (0,0), colspan=2, rowspan=3)
    Call the function plt.subplot2grid()
    Specify the size of the figure’s overall grid, which is 3 rows and 3 columns (3,3)
    Specify the location of the large subplot: start counting from row 0 column 0 (0,0)
    Make a subplot across 2 columns and 3 rows colspan=2, rowspan=3.

    2):
    https://stackoverflow.com/questions/13128647/matplotlib-finance-volume-overlay/13216161
    https://zhuanlan.zhihu.com/p/28584048
'''
################################################################################


def bbands(cus_ticker_list):
    print("*******************************************************")
    print("Running Bollinger Bands...")
    print("Get BBands on:")
    print("1) Stocks")
    print("2) User Portfolio")
    ope = input()
    if ope == '1':
        print("Stock ticker(e.g. 0001.HK): ")
        ticker = stock.tick_process(input("[Type 'hk' for Hong Kong tickers; 'us' for USA; 'cn' for China]"))
        if ticker == 'hk':
            stock.check_ticker_by_country('Hong Kong')
        elif ticker == 'us':
            stock.check_ticker_by_country('USA')
        elif ticker == 'cn':
            stock.check_ticker_by_country('China')
        elif ticker == '':
            print("Invalid ticker!")
        else:
            print("\n")
            cal_plot_bband(ticker)
    elif ope == '2':
        if len(cus_ticker_list) > 0:
            for tk in cus_ticker_list:
                cal_plot_bband(tk)
        else:
            print("No stock data!")

    print("Finish")
    print("\n")
