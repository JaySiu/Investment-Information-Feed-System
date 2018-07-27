'''
RMs can select different indicators for doing the technical analysis
for the clients
'''

import time
from macd import macd
#from bbands import bbands

indicators = {'1': 'B-Bands', '2': 'CCI', '3':'KDJ', '4': 'MACD', '5':'RSI'}

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
    choices = input().split(',')
    if len(choices) > len(indicators) or len(list(set(choices)-set(indicators.keys()))) > 0:
        print("Invalid input!")
    else:
        for c in choices:
            c = c.strip()
            if indicators[c] == 'B-Bands':
                #bbands()
                print("B-Bands")
            elif indicators[c] == 'CCI'
                print("CCI")
            elif indicators[c] == 'KDJ':
                print("KDJ")
            elif indicators[c] == 'MACD':
                macd()
            elif indicators[c] == 'RSI':
                print("RSI")


if __name__ == '__main__':
    analyze()
