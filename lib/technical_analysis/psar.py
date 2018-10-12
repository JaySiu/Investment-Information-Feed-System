'''
Parabolic Stop and Reverse
'''

import talib
import stock
import matplotlib
import matplotlib.pyplot as plt

##### helper ###################################################################

def cal_plot_psar(ticker, step=0.02, max_step=0.2):
    print("Calculating Parabolic SAR...")
    stock_data = stock.stock_preprocess_arr_list(ticker)
    psar = talib.SAR(stock_data[3], stock_data[4], acceleration=step, maximum=max_step)

    ##### plotting
    fig, ax = plt.subplots(1, 1, figsize=(15,15))
    name = stock.check_all_ticker(ticker)[0]
    plt.suptitle('Parabolic Stop and Reverse of {}({})'.format(name, ticker), fontsize = 20, fontweight='bold')

    ax.plot(stock_data[0], stock_data[2], label='Price - '+name, color='black')
    ax.plot(stock_data[0], psar, '.', label='Parabloic SAR', color='#708EB2')

    ax.grid(True)
    ax.legend()
    ax.minorticks_on()
    ax.tick_params(axis='x',which='minor',bottom='off')

    fig.tight_layout()
    fig.subplots_adjust(top=0.95)
    #plt.show()
    stock.save_plot('PSAR', ticker)

################################################################################

def psar(cus_ticker_list):
    print("*******************************************************")
    print("Running Parabolic Stop and Reverse...")
    print("Get Parabolic SAR on:")
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
            print("Enter the Step and Max. Step (sepearted by ','):")
            step_max_step = input("[Enter d to use default: .02, .2] ")
            if step_max_step == 'd':
                cal_plot_psar(ticker)
            else:
                step, max_step =  step_max_step.split(',')
                step = step.strip().replace('.','',1)
                max_step = max_step.strip().replace('.','',1)
                if step.isdigit() and max_step.isdigit():
                    cal_plot_psar(ticker, float(step), float(max_step))
                else:
                    print("Invalid Input!")
    elif ope == '2':
        print("Enter the Step and Max. Step (sepearted by ','):")
        step_max_step = input("[Enter d to use default: .02, .2] ")
        if step_max_step == 'd':
            if len(cus_ticker_list) > 0:
                for tk in cus_ticker_list:
                    cal_plot_psar(tk)
            else:
                    print("No stock data!")
        else:
            step, max_step =  step_max_step.split(',')
            step = step.strip().replace('.','',1)
            max_step = max_step.strip().replace('.','',1)
            if step.isdigit() and max_step.isdigit():
                if len(cus_ticker_list) > 0:
                    for tk in cus_ticker_list:
                        cal_plot_psar(tk, float(step), float(max_step))
                else:
                        print("No stock data!")
            else:
                print("Invalid Input!")
    print("Finish")
    print("\n")
