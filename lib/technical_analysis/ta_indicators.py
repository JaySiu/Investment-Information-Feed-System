'''
RMs can select different indicators for doing the technical analysis
for the clients

Plotting the graphs requires the data to be passed in asc order
'''

import time
import ta_user_portfolio as taup
from bbands import bbands
from cci import cci
from kdj import kdj
from macd import macd
from obv import obv
from psar import psar
from rsi import rsi

INDICATORS = {'1': 'B-Bands', '2': 'CCI', '3':'KDJ', '4': 'MACD', '5': 'OBV', '6': 'Parabolic SAR', '7':'RSI'}

def technical_analyze():
    print("*******************************************************")
    print("Enter your client\'s id (number only):")
    cus_id = input()
    cus_ticker_list = taup.get_client_tickers(cus_id)
    if cus_ticker_list == None or cus_ticker_list == []:
        print("Customer data not found!")
        cus_ticker_list = []
    print("*******************************************************")
    print("Select indicators:(choices separated by ',' e.g. 1,2,3)")
    keys = list(INDICATORS.keys())
    keys.sort()
    for k in keys:
        print("{}) {}".format(k, INDICATORS.get(k)))
    choices = [c.strip() for c in input().split(',')]
    if len(choices) > len(INDICATORS) or len(list(set(choices)-set(INDICATORS.keys()))) > 0:
        print("Invalid input!")
    else:
        for c in choices:
            if INDICATORS[c] == 'B-Bands':
                bbands(cus_ticker_list)
            elif INDICATORS[c] == 'CCI':
                cci(cus_ticker_list)
            elif INDICATORS[c] == 'KDJ':
                kdj(cus_ticker_list)
            elif INDICATORS[c] == 'MACD':
                macd(cus_ticker_list)
            elif INDICATORS[c] == 'OBV':
                obv(cus_ticker_list)
            elif INDICATORS[c] == 'Parabolic SAR':
                psar(cus_ticker_list)
            elif INDICATORS[c] == 'RSI':
                rsi(cus_ticker_list)


if __name__ == '__main__':
    technical_analyze()
