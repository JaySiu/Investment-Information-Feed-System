'''
(Slow) Stochastic Oscillator with J Line
'''

import talib
import stock
import matplotlib
import matplotlib.pyplot as plt

##### helper ###################################################################

def cal_plot_kdj(ticker):
    print("Calculating KDJ...")
    stock_data = stock.stock_preprocess_arr_list(ticker)
    k, d = talib.STOCH(stock_data[3], stock_data[4], stock_data[2], fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    j = 3*k - 2*d

    ##### plotting
    fig, ax_list = plt.subplots(2, 1, figsize=(15,15))
    name = stock.check_all_ticker(ticker)[0]
    plt.suptitle('Stochastic with J Line of {}({})'.format(name, ticker), fontsize = 20, fontweight='bold')

    ax_list[0].plot(stock_data[0], stock_data[2], label='Price - '+name, color='black')
    ax_list[0].get_xaxis().set_visible(False)

    ax_list[1].plot(stock_data[0], k, label='%K', color='#DC9F86')
    ax_list[1].plot(stock_data[0], d, label='%D', color='#13F90D')
    ax_list[1].plot(stock_data[0], j, label='%J', color='#E06FC4')

    for i in range(2):
        ax_list[i].grid(True)
        ax_list[i].legend()
        ax_list[i].minorticks_on()
        ax_list[i].tick_params(axis='x',which='minor',bottom='off')

    fig.tight_layout()
    fig.subplots_adjust(hspace=0, top=0.95)
    #plt.show()
    stock.save_plot('KDJ', ticker)

################################################################################

def kdj(cus_ticker_list):
    print("*******************************************************")
    print("Running Stochastic with %J...")
    print("Get KDJ on:")
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
            cal_plot_kdj(ticker)
    elif ope == '2':
        if len(cus_ticker_list) > 0:
            for tk in cus_ticker_list:
                cal_plot_kdj(tk)
        else:
            print("No stock data!")

    print("Finish")
    print("\n")
