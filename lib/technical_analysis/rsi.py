'''
Relative Strength Index
'''

import talib
import stock
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

##### helper ###################################################################

def cal_plot_rsi(ticker):
    print("Calculating RSI...")
    stock_data = stock.stock_preprocess_arr_list(ticker)
    rsi = talib.RSI(stock_data[2], timeperiod=14)

    ##### plotting
    fig, ax = plt.subplots(1, 1, figsize=(15,15))
    plt.suptitle('Relative Strength Index of {}({})'.format(stock.check_all_ticker(ticker), ticker), fontsize = 20, fontweight='bold')
    ax.plot(stock_data[0], rsi, label='RSI', color='#A139B3')
    ax.fill_between(stock_data[0], 70, 30, color='#DED3E5')

    ax.legend()
    ax.grid(True)
    ax.minorticks_on()
    ax.tick_params(axis='x',which='minor',bottom='off')
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%b'))

    fig.tight_layout()
    fig.subplots_adjust(top=0.95)
    plt.show()

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
