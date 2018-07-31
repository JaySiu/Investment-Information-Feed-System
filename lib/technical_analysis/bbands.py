'''
Bollinger Bands (B-Bands)
'''
import time
import talib
import stock
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ochl, volume_overlay

##### helpers ##################################################################

def cal_plot_bband(ticker):
    print("Calculating Bollinger Bands...")
    stock_data = stock.stock_preprocess_candlestick(ticker)
    upper, middle, lower = talib.BBANDS(stock_data[2], matype=talib.MA_Type.SMA)

    ##### ploting
    fig, ax_list = plt.subplots(2, 1, figsize=(15,15))
    plt.suptitle('Bollinger Bands of {}({})'.format(stock.check_all_ticker(ticker), ticker), fontsize = 20, fontweight='bold')

    candlestick_ochl(ax_list[0], stock_data[0], width=0.8, colorup='#53B987', colordown='#EB4D5C')
    ax_list[0].xaxis.set_major_locator(mdates.MonthLocator())
    ax_list[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d'))
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
    plt.setp(plt.gca().get_xticklabels(), rotation=40)
    fig.subplots_adjust(hspace=0)
    plt.show()

################################################################################


def bbands():
    print("*******************************************************")
    print("Running BBands...")
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
        else:
            print("\n")
            cal_plot_bband(ticker)

    print("Finish")
    print("\n")
