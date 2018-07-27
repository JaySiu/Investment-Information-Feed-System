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

##### helpers ##################################################################

#def cal_bband(ticker):



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
        ticker = input("[Type 'hk' for Hong Kong tickers; 'us' for USA; 'cn' for China]")
        if ticker.lower() == 'hk':
            stock.check_ticker_by_country('Hong Kong')
        elif ticker.lower() == 'us':
            stock.check_ticker_by_country('USA')
        elif ticker.lower() == 'cn':
            stock.check_ticker_by_country('China')
        else:
            print("\n")
            print("[Enter d to use default: 12(fast), 26(slow), 9(signal)]")
            fast = input("Fast period: (days)").lower()
            if fast == 'd':
                print("\n")

            elif fast.isdigit():
                slow = input("Slow period: (days)")
                signal = input("Signal: (days)")
                print("\n")

            else:
                print("Error!")

    print("Finish")
    print("\n")
