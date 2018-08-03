'''
RMs can select different indicators for doing the technical analysis
for the clients
'''

import time
from bbands import bbands
from cci import cci
from kdj import kdj
from macd import macd
from obv import obv
from rsi import rsi


indicators = {'1': 'B-Bands', '2': 'CCI', '3':'KDJ', '4': 'MACD', '5': 'OBV', '6': 'Parabolic SAR', '7':'RSI'}

def analyze():
    print("*******************************************************")
    print("Enter your client\'s id:")
    id = input()
    print("*******************************************************")
    print("Select indicators:(choices separated by ',' e.g. 1,2,3)")
    keys = list(indicators.keys())
    keys.sort()
    for k in keys:
        print("{}) {}".format(k, indicators.get(k)))
    choices = [c.strip() for c in input().split(',')]
    if len(choices) > len(indicators) or len(list(set(choices)-set(indicators.keys()))) > 0:
        print("Invalid input!")
    else:
        for c in choices:
            if indicators[c] == 'B-Bands':
                bbands()
            elif indicators[c] == 'CCI':
                cci()
            elif indicators[c] == 'KDJ':
                kdj()
            elif indicators[c] == 'MACD':
                macd()
            elif indicators[c] == 'OBV':
                obv()
            elif indicators[c] == 'Parabolic SAR':
                print("PSAR")
            elif indicators[c] == 'RSI':
                rsi()


if __name__ == '__main__':
    analyze()
