'''
RMs can select different indicators for doing the technical analysis
for the clients
'''

import time
from bbands import bbands
from macd import macd
from rsi import rsi


indicators = {'1': 'B-Bands', '2': 'CCI', '3':'KDJ', '4': 'MACD', '5': 'OBV', '6':'RSI'}

def analyze():
    print("*******************************************************")
    print("Enter your client\'s id:")
    id = input()
    print("*******************************************************")
    print("Select indicators:(choices separated by \',\')")
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
                print("Commodity Channel Index")
            elif indicators[c] == 'KDJ':
                print("KDJ")
            elif indicators[c] == 'MACD':
                macd()
            elif indicators[c] == 'OBV':
                print("On-Balance Volume")
            elif indicators[c] == 'RSI':
                rsi()


if __name__ == '__main__':
    analyze()
