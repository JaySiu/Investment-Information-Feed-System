'''

'''

import talib
import stock
import matplotlib.pyplot as plt

##### helper ###################################################################

def cal_plot_rsi(ticker):
    print("Calculating RSI...")
    stock_data = stock.stock_preprocess_arr_list(ticker)
    rsi = talib.RSI(stock_data[2], timeperiod=14)

    ##### plotting
    fig, ax_list = plt.subplots(1, 1, figsize=(15,15))
    plt.suptitle('Relative Strength Index of {}({})'.format(stock.check_all_ticker(ticker), ticker), fontsize = 20, fontweight='bold')


################################################################################

def rsi():
    print("*******************************************************")
    print("Running Relative Strength Index...")
    print("Get RSI on:")
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
            cal_plot_rsi(ticker)

    print("Finish")
    print("\n")
