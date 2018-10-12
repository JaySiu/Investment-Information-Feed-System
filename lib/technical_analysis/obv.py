'''
On-Balance Volume
'''

import talib
import stock
import matplotlib
import matplotlib.pyplot as plt

##### helper ###################################################################

def cal_plot_obv(ticker):
    print("Calculating OBV...")
    stock_data = stock.stock_preprocess_arr_list(ticker)
    obv = talib.OBV(stock_data[2], stock_data[5].astype(float))

    ##### plotting
    fig, ax_list = plt.subplots(2, 1, figsize=(15,15))
    name = stock.check_all_ticker(ticker)[0]
    plt.suptitle('On-Balance Volume {}({})'.format(name, ticker), fontsize = 20, fontweight='bold')

    ax_list[0].plot(stock_data[0], stock_data[2], label='Price - '+name, color='black')
    ax_list[0].get_xaxis().set_visible(False)

    ax_list[1].plot(stock_data[0], obv, label='OBV', color='#BB9F6D')

    for i in range(2):
        ax_list[i].grid(True)
        ax_list[i].legend()
        ax_list[i].minorticks_on()
        ax_list[i].tick_params(axis='x',which='minor',bottom='off')

    fig.tight_layout()
    fig.subplots_adjust(hspace=0, top=0.95)
    #plt.show()
    stock.save_plot('OBV', ticker)

################################################################################

def obv(cus_ticker_list):
    print("*******************************************************")
    print("Running On-Balance Value...")
    print("Get OBV on:")
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
            cal_plot_obv(ticker)
    elif ope == '2':
        if len(cus_ticker_list) > 0:
            for tk in cus_ticker_list:
                cal_plot_obv(tk)
        else:
            print("No stock data!")

    print("Finish")
    print("\n")
